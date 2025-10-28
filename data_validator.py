#!/usr/bin/env python3
"""
Data Validation Module for DBF Files
Provides comprehensive data quality analysis and validation features
"""

import hashlib
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import re


class DBFDataValidator:
    """Comprehensive data validation and quality analysis for DBF files"""
    
    def __init__(self, dbf_records, field_info, encoding_used='unknown'):
        self.records = list(dbf_records)  # Convert to list for multiple iterations
        self.field_info = field_info
        self.encoding_used = encoding_used
        self.total_records = len(self.records)
        
        # Validation results
        self.validation_results = {
            'duplicates': {},
            'field_analysis': {},
            'data_types': {},
            'missing_data': {},
            'encoding_confidence': {},
            'quality_score': 0,
            'summary': {}
        }
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete data validation analysis"""
        print("🔍 Starting comprehensive data validation...")
        
        # Run all validation checks
        self._detect_duplicates()
        self._analyze_fields()
        self._validate_data_types()
        self._analyze_missing_data()
        self._calculate_encoding_confidence()
        self._calculate_quality_score()
        self._generate_summary()
        
        print("✅ Data validation completed!")
        return self.validation_results
    
    def _detect_duplicates(self):
        """Detect duplicate records"""
        print("🔎 Detecting duplicate records...")
        
        record_hashes = defaultdict(list)
        duplicates = []
        
        for idx, record in enumerate(self.records):
            # Create hash of record content (excluding None values for better matching)
            clean_record = {k: v for k, v in record.items() if v is not None}
            record_str = str(sorted(clean_record.items()))
            record_hash = hashlib.md5(record_str.encode('utf-8', errors='ignore')).hexdigest()
            
            record_hashes[record_hash].append(idx)
        
        # Find duplicates
        for record_hash, indices in record_hashes.items():
            if len(indices) > 1:
                duplicates.append({
                    'hash': record_hash,
                    'record_indices': indices,
                    'count': len(indices),
                    'sample_record': dict(self.records[indices[0]])
                })
        
        self.validation_results['duplicates'] = {
            'total_duplicates': len(duplicates),
            'total_duplicate_records': sum(dup['count'] for dup in duplicates),
            'duplicate_percentage': (sum(dup['count'] for dup in duplicates) / self.total_records * 100) if self.total_records > 0 else 0,
            'duplicate_groups': duplicates[:10]  # Limit to first 10 for display
        }
    
    def _analyze_fields(self):
        """Analyze field characteristics"""
        print("📊 Analyzing field characteristics...")
        
        field_stats = {}
        
        for field in self.field_info:
            field_name = field['name']
            field_stats[field_name] = {
                'type': field.get('type', 'Unknown'),
                'length': field.get('length', 0),
                'null_count': 0,
                'unique_count': 0,
                'min_length': float('inf'),
                'max_length': 0,
                'sample_values': set(),
                'pattern_analysis': {},
                'value_distribution': Counter()
            }
        
        # Analyze each record
        for record in self.records:
            for field_name in field_stats:
                value = record.get(field_name)
                stats = field_stats[field_name]
                
                if value is None or value == '':
                    stats['null_count'] += 1
                else:
                    value_str = str(value).strip()
                    value_len = len(value_str)
                    
                    stats['min_length'] = min(stats['min_length'], value_len)
                    stats['max_length'] = max(stats['max_length'], value_len)
                    
                    # Sample values (limit to 20)
                    if len(stats['sample_values']) < 20:
                        stats['sample_values'].add(value_str[:50])  # Truncate long values
                    
                    # Value distribution (for categorical analysis)
                    if value_len < 100:  # Only for reasonable-length values
                        stats['value_distribution'][value_str] += 1
        
        # Calculate final statistics
        for field_name, stats in field_stats.items():
            stats['sample_values'] = list(stats['sample_values'])
            stats['unique_count'] = len(stats['value_distribution'])
            stats['fill_rate'] = ((self.total_records - stats['null_count']) / self.total_records * 100) if self.total_records > 0 else 0
            
            if stats['min_length'] == float('inf'):
                stats['min_length'] = 0
            
            # Determine if field appears to be categorical
            stats['appears_categorical'] = (
                stats['unique_count'] < self.total_records * 0.1 and 
                stats['unique_count'] < 100
            )
            
            # Pattern analysis for common formats
            stats['pattern_analysis'] = self._analyze_field_patterns(stats['sample_values'])
        
        self.validation_results['field_analysis'] = field_stats
    
    def _analyze_field_patterns(self, sample_values: List[str]) -> Dict[str, Any]:
        """Analyze common patterns in field values"""
        patterns = {
            'email_like': 0,
            'phone_like': 0,
            'date_like': 0,
            'numeric_like': 0,
            'postal_code_like': 0,
            'german_characters': 0
        }
        
        for value in sample_values:
            if not value:
                continue
                
            # Email pattern
            if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', value):
                patterns['email_like'] += 1
            
            # Phone pattern (various formats)
            if re.search(r'[\+]?[\d\s\-\(\)]{7,}', value):
                patterns['phone_like'] += 1
            
            # Date pattern
            if re.search(r'\d{1,2}[\.\/\-]\d{1,2}[\.\/\-]\d{2,4}', value):
                patterns['date_like'] += 1
            
            # Numeric pattern
            if re.search(r'^\d+(\.\d+)?$', value):
                patterns['numeric_like'] += 1
            
            # German postal code
            if re.search(r'^\d{5}$', value):
                patterns['postal_code_like'] += 1
            
            # German characters
            if re.search(r'[äöüßÄÖÜ]', value):
                patterns['german_characters'] += 1
        
        return patterns
    
    def _validate_data_types(self):
        """Validate data type consistency"""
        print("🔬 Validating data type consistency...")
        
        type_issues = {}
        
        for field in self.field_info:
            field_name = field['name']
            expected_type = field.get('type', 'C')  # Default to character
            issues = []
            
            for idx, record in enumerate(self.records):
                value = record.get(field_name)
                if value is None:
                    continue
                
                # Check type consistency based on DBF field type
                issue = self._check_type_consistency(value, expected_type, idx)
                if issue:
                    issues.append(issue)
                    if len(issues) >= 10:  # Limit examples
                        break
            
            if issues:
                type_issues[field_name] = {
                    'expected_type': expected_type,
                    'issue_count': len(issues),
                    'examples': issues
                }
        
        self.validation_results['data_types'] = type_issues
    
    def _check_type_consistency(self, value, expected_type: str, record_idx: int) -> Optional[Dict]:
        """Check if value matches expected DBF field type"""
        value_str = str(value).strip()
        
        if expected_type == 'N' and not re.match(r'^-?\d*\.?\d*$', value_str):
            return {
                'record_index': record_idx,
                'value': value_str[:50],
                'issue': 'Non-numeric value in numeric field'
            }
        elif expected_type == 'D' and not re.match(r'^\d{8}$', value_str):
            if value_str and value_str != '00000000':
                return {
                    'record_index': record_idx,
                    'value': value_str[:50],
                    'issue': 'Invalid date format (expected YYYYMMDD)'
                }
        elif expected_type == 'L' and value_str.upper() not in ['T', 'F', 'Y', 'N', '']:
            return {
                'record_index': record_idx,
                'value': value_str[:50],
                'issue': 'Invalid logical value (expected T/F/Y/N)'
            }
        
        return None
    
    def _analyze_missing_data(self):
        """Analyze missing data patterns"""
        print("📋 Analyzing missing data patterns...")
        
        missing_stats = {}
        
        for field in self.field_info:
            field_name = field['name']
            null_count = 0
            empty_count = 0
            
            for record in self.records:
                value = record.get(field_name)
                if value is None:
                    null_count += 1
                elif str(value).strip() == '':
                    empty_count += 1
            
            total_missing = null_count + empty_count
            missing_percentage = (total_missing / self.total_records * 100) if self.total_records > 0 else 0
            
            missing_stats[field_name] = {
                'null_count': null_count,
                'empty_count': empty_count,
                'total_missing': total_missing,
                'missing_percentage': missing_percentage,
                'completeness_score': 100 - missing_percentage
            }
        
        self.validation_results['missing_data'] = missing_stats
    
    def _calculate_encoding_confidence(self):
        """Calculate encoding detection confidence"""
        print("🌍 Calculating encoding confidence...")
        
        # Test the data with different encodings and measure "quality"
        encodings_to_test = ['cp1252', 'iso-8859-1', 'cp850', 'utf-8', 'latin1']
        confidence_scores = {}
        
        # Sample some text data for testing
        sample_text = []
        for record in self.records[:100]:  # Test first 100 records
            for value in record.values():
                if isinstance(value, str) and len(value) > 5:
                    sample_text.append(value)
                    if len(sample_text) >= 50:
                        break
            if len(sample_text) >= 50:
                break
        
        for encoding in encodings_to_test:
            score = self._test_encoding_quality(sample_text, encoding)
            confidence_scores[encoding] = score
        
        # Determine confidence for the encoding used
        used_encoding_confidence = confidence_scores.get(self.encoding_used, 0)
        
        self.validation_results['encoding_confidence'] = {
            'encoding_used': self.encoding_used,
            'confidence_score': used_encoding_confidence,
            'confidence_level': self._get_confidence_level(used_encoding_confidence),
            'alternative_encodings': sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True),
            'recommendation': self._get_encoding_recommendation(confidence_scores, self.encoding_used)
        }
    
    def _test_encoding_quality(self, sample_text: List[str], encoding: str) -> float:
        """Test quality of text with given encoding"""
        if not sample_text:
            return 0
        
        quality_score = 0
        total_chars = 0
        
        for text in sample_text:
            try:
                # Try to encode/decode
                encoded = text.encode(encoding, errors='ignore')
                decoded = encoded.decode(encoding, errors='ignore')
                
                # Calculate quality metrics
                char_retention = len(decoded) / len(text) if text else 0
                has_german_chars = bool(re.search(r'[äöüßÄÖÜ]', decoded))
                no_replacement_chars = '�' not in decoded
                
                quality_score += char_retention * 40  # 40% weight for character retention
                if has_german_chars:
                    quality_score += 30  # 30% bonus for German character support
                if no_replacement_chars:
                    quality_score += 30  # 30% bonus for no replacement characters
                
                total_chars += len(text)
                
            except Exception:
                continue
        
        return quality_score / len(sample_text) if sample_text else 0
    
    def _get_confidence_level(self, score: float) -> str:
        """Convert numeric confidence to descriptive level"""
        if score >= 80:
            return "High"
        elif score >= 60:
            return "Medium"
        elif score >= 40:
            return "Low"
        else:
            return "Very Low"
    
    def _get_encoding_recommendation(self, confidence_scores: Dict[str, float], current_encoding: str) -> str:
        """Generate encoding recommendation"""
        best_encoding, best_score = max(confidence_scores.items(), key=lambda x: x[1])
        current_score = confidence_scores.get(current_encoding, 0)
        
        if best_score > current_score + 20:  # Significant improvement
            return f"Consider using '{best_encoding}' (score: {best_score:.1f}) instead of '{current_encoding}' (score: {current_score:.1f})"
        elif current_score >= 80:
            return f"Current encoding '{current_encoding}' is optimal"
        else:
            return f"Current encoding '{current_encoding}' may have issues. Best alternative: '{best_encoding}'"
    
    def _calculate_quality_score(self):
        """Calculate overall data quality score"""
        print("🏆 Calculating overall quality score...")
        
        scores = []
        
        # Duplicate score (lower duplicates = higher score)
        duplicate_rate = self.validation_results['duplicates']['duplicate_percentage']
        duplicate_score = max(0, 100 - duplicate_rate * 2)  # Penalize duplicates heavily
        scores.append(('duplicates', duplicate_score, 20))  # 20% weight
        
        # Completeness score (average fill rate across fields)
        if self.validation_results['missing_data']:
            avg_completeness = sum(
                field['completeness_score'] 
                for field in self.validation_results['missing_data'].values()
            ) / len(self.validation_results['missing_data'])
            scores.append(('completeness', avg_completeness, 30))  # 30% weight
        
        # Encoding confidence score
        encoding_score = self.validation_results['encoding_confidence']['confidence_score']
        scores.append(('encoding', encoding_score, 25))  # 25% weight
        
        # Data type consistency score
        type_issue_count = len(self.validation_results['data_types'])
        total_fields = len(self.field_info)
        type_score = max(0, 100 - (type_issue_count / total_fields * 100)) if total_fields > 0 else 100
        scores.append(('data_types', type_score, 25))  # 25% weight
        
        # Calculate weighted average
        weighted_score = sum(score * weight for _, score, weight in scores) / 100
        
        self.validation_results['quality_score'] = {
            'overall_score': weighted_score,
            'grade': self._get_quality_grade(weighted_score),
            'component_scores': {name: score for name, score, _ in scores}
        }
    
    def _get_quality_grade(self, score: float) -> str:
        """Convert numeric quality score to letter grade"""
        if score >= 90:
            return "A (Excellent)"
        elif score >= 80:
            return "B (Good)"
        elif score >= 70:
            return "C (Fair)"
        elif score >= 60:
            return "D (Poor)"
        else:
            return "F (Very Poor)"
    
    def _generate_summary(self):
        """Generate executive summary of validation results"""
        summary = {
            'total_records': self.total_records,
            'total_fields': len(self.field_info),
            'overall_quality': self.validation_results['quality_score']['grade'],
            'key_findings': [],
            'recommendations': []
        }
        
        # Key findings
        if self.validation_results['duplicates']['total_duplicates'] > 0:
            summary['key_findings'].append(
                f"Found {self.validation_results['duplicates']['total_duplicates']} duplicate record groups"
            )
        
        if self.validation_results['data_types']:
            summary['key_findings'].append(
                f"Data type inconsistencies found in {len(self.validation_results['data_types'])} fields"
            )
        
        # Recommendations
        if self.validation_results['duplicates']['duplicate_percentage'] > 5:
            summary['recommendations'].append("Consider removing duplicate records before processing")
        
        if self.validation_results['encoding_confidence']['confidence_score'] < 70:
            summary['recommendations'].append(
                self.validation_results['encoding_confidence']['recommendation']
            )
        
        self.validation_results['summary'] = summary


def validate_dbf_file(dbf_path: str, encoding: str = None) -> Dict[str, Any]:
    """
    Convenience function to validate a DBF file
    
    Args:
        dbf_path: Path to the DBF file
        encoding: Encoding to use (if None, will try to detect)
    
    Returns:
        Validation results dictionary
    """
    from dbfread import DBF
    
    # Try to open DBF file
    encodings_to_try = [encoding] if encoding else ['cp1252', 'iso-8859-1', 'cp850', 'utf-8']
    
    for enc in encodings_to_try:
        if enc is None:
            continue
        try:
            dbf = DBF(dbf_path, encoding=enc, char_decode_errors='ignore')
            records = list(dbf)
            field_info = [{'name': f.name, 'type': f.type, 'length': f.length} for f in dbf.fields]
            
            # Run validation
            validator = DBFDataValidator(records, field_info, enc)
            return validator.run_full_validation()
            
        except Exception as e:
            print(f"Failed to read with encoding {enc}: {e}")
            continue
    
    raise Exception("Could not read DBF file with any supported encoding")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python data_validator.py <dbf_file> [encoding]")
        sys.exit(1)
    
    dbf_file = sys.argv[1]
    encoding = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        results = validate_dbf_file(dbf_file, encoding)
        
        print("\n" + "="*60)
        print("📊 DBF DATA VALIDATION REPORT")
        print("="*60)
        
        summary = results['summary']
        print(f"📁 File: {dbf_file}")
        print(f"📊 Records: {summary['total_records']:,}")
        print(f"📋 Fields: {summary['total_fields']}")
        print(f"🏆 Quality Grade: {summary['overall_quality']}")
        
        if summary['key_findings']:
            print(f"\n🔍 Key Findings:")
            for finding in summary['key_findings']:
                print(f"  • {finding}")
        
        if summary['recommendations']:
            print(f"\n💡 Recommendations:")
            for rec in summary['recommendations']:
                print(f"  • {rec}")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)