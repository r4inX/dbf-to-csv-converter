#!/usr/bin/python

import argparse
import csv
import sys
from pathlib import Path

from dbfread import DBF


def convert_dbf_to_csv(input_file, output_file=None, delimiter=";", encoding="utf-8", validate=False, validation_report=None):
    """
    Convert DBF file to CSV with proper error handling and data cleaning
    
    Args:
        input_file: Path to DBF file
        output_file: Path to output CSV file
        delimiter: CSV delimiter
        encoding: Output encoding
        validate: Whether to run data validation
        validation_report: Path to save validation report
    """
    try:
        # Validate input file
        if not Path(input_file).exists():
            raise FileNotFoundError(f"Input file '{input_file}' not found")

        if not input_file.lower().endswith(".dbf"):
            raise ValueError(f"Input file '{input_file}' is not a .dbf file")

        # Set output filename if not provided
        if output_file is None:
            output_file = input_file[:-4] + ".csv"

        # Check if output file already exists and warn user
        if Path(output_file).exists():
            print(
                f"Warning: Output file '{output_file}' already exists "
                "and will be overwritten"
            )

        print(f"Converting '{input_file}' to '{output_file}'")

        # Open and process the DBF file
        with open(output_file, "w", newline="", encoding=encoding) as csvfile:
            try:
                # Try cp1252 first (Windows German codepage)
                # Most common for German DBF files
                in_db = DBF(input_file, encoding="cp1252")
            except UnicodeDecodeError:
                try:
                    # Try iso-8859-1 (Latin-1, includes German characters)
                    in_db = DBF(input_file, encoding="iso-8859-1")
                except UnicodeDecodeError:
                    try:
                        # Try cp850 (DOS German codepage)
                        in_db = DBF(input_file, encoding="cp850")
                    except UnicodeDecodeError:
                        try:
                            # Try cp437 (original IBM PC codepage)
                            in_db = DBF(input_file, encoding="cp437")
                        except UnicodeDecodeError:
                            # Fallback to UTF-8
                            in_db = DBF(input_file, encoding="utf-8")

            out_csv = csv.writer(csvfile, delimiter=delimiter, quoting=csv.QUOTE_ALL)

            # Write header row
            names = []
            for field in in_db.fields:
                names.append(field.name)
            out_csv.writerow(names)

            # Process records with progress indication
            record_count = 0
            for rec in in_db:
                # Clean up line breaks and other problematic characters in each field
                cleaned_values = []
                for value in rec.values():
                    if value is None:
                        cleaned_values.append("")
                    elif isinstance(value, str):
                        # Replace line breaks with spaces and clean up other whitespace
                        cleaned_value = (
                            value.replace("\n", " ")
                            .replace("\r", " ")
                            .replace("\t", " ")
                        )
                        # Remove multiple consecutive spaces
                        cleaned_value = " ".join(cleaned_value.split())
                        # Remove any remaining problematic characters
                        cleaned_value = cleaned_value.replace("\x00", "").replace(
                            "\x1a", ""
                        )
                        cleaned_values.append(cleaned_value)
                    else:
                        cleaned_values.append(value)

                out_csv.writerow(cleaned_values)
                record_count += 1

                # Show progress every 1000 records
                if record_count % 1000 == 0:
                    print(f"Processed {record_count} records...")

            print(
                f"Conversion completed successfully! Processed {record_count} records."
            )
            
            # Run validation if requested
            if validate:
                print("\n" + "="*50)
                print("🔍 Running data validation analysis...")
                print("="*50)
                
                try:
                    from data_validator import DBFDataValidator
                    
                    # Re-read the DBF file for validation
                    validation_records = []
                    validation_dbf = None
                    
                    # Try the same encoding sequence as conversion
                    for encoding_attempt in ['cp1252', 'iso-8859-1', 'cp850', 'cp437', 'utf-8']:
                        try:
                            validation_dbf = DBF(input_file, encoding=encoding_attempt)
                            validation_records = list(validation_dbf)
                            used_encoding = encoding_attempt
                            break
                        except UnicodeDecodeError:
                            continue
                    
                    if validation_dbf and validation_records:
                        field_info = [{'name': f.name, 'type': f.type, 'length': f.length} for f in validation_dbf.fields]
                        
                        # Run validation
                        validator = DBFDataValidator(validation_records, field_info, used_encoding)
                        validation_results = validator.run_full_validation()
                        
                        # Print summary
                        summary = validation_results['summary']
                        print(f"📊 Quality Grade: {summary['overall_quality']}")
                        print(f"🔍 Duplicates: {validation_results['duplicates']['total_duplicates']} groups")
                        print(f"🌍 Encoding Confidence: {validation_results['encoding_confidence']['confidence_level']}")
                        
                        if summary['key_findings']:
                            print("\n🔍 Key Findings:")
                            for finding in summary['key_findings'][:3]:  # Limit to 3
                                print(f"  • {finding}")
                        
                        if summary['recommendations']:
                            print("\n💡 Recommendations:")
                            for rec in summary['recommendations'][:3]:  # Limit to 3
                                print(f"  • {rec}")
                        
                        # Save detailed report if requested
                        if validation_report:
                            import json
                            with open(validation_report, 'w', encoding='utf-8') as f:
                                json.dump(validation_results, f, indent=2, default=str)
                            print(f"\n📄 Detailed validation report saved to: {validation_report}")
                    
                except ImportError:
                    print("⚠️  Data validation module not available")
                except Exception as e:
                    print(f"⚠️  Validation failed: {e}")
                
                print("="*50)
            
            return True

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
        return False
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False


def main():
    # Add command line argument parsing for better usability
    parser = argparse.ArgumentParser(description="Convert DBF files to CSV format with optional data validation")
    parser.add_argument("input_file", help="Path to the input DBF file")
    parser.add_argument("-o", "--output", help="Path to the output CSV file (optional)")
    parser.add_argument(
        "-d", "--delimiter", default=";", help="CSV delimiter (default: semicolon)"
    )
    parser.add_argument(
        "-e", "--encoding", default="utf-8", help="Output encoding (default: utf-8)"
    )
    parser.add_argument(
        "--validate", action="store_true", help="Run data quality validation analysis"
    )
    parser.add_argument(
        "--validation-report", help="Save detailed validation report to JSON file"
    )

    # Parse arguments
    args = parser.parse_args()
    success = convert_dbf_to_csv(
        args.input_file, 
        args.output, 
        args.delimiter, 
        args.encoding,
        args.validate,
        args.validation_report
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
