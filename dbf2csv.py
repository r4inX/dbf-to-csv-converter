#!/usr/bin/python

import csv
from dbfread import DBF
import os
import sys
import argparse
from pathlib import Path

def convert_dbf_to_csv(input_file, output_file=None, delimiter=';', encoding='utf-8'):
    """
    Convert DBF file to CSV with proper error handling and data cleaning
    """
    try:
        # Validate input file
        if not Path(input_file).exists():
            raise FileNotFoundError(f"Input file '{input_file}' not found")
        
        if not input_file.lower().endswith('.dbf'):
            raise ValueError(f"Input file '{input_file}' is not a .dbf file")
        
        # Set output filename if not provided
        if output_file is None:
            output_file = input_file[:-4] + ".csv"
        
        # Check if output file already exists and warn user
        if Path(output_file).exists():
            print(f"Warning: Output file '{output_file}' already exists and will be overwritten")
        
        print(f"Converting '{input_file}' to '{output_file}'")
        
        # Open and process the DBF file
        with open(output_file, 'w', newline='', encoding=encoding) as csvfile:
            try:
                # Try cp1252 first (Windows German codepage, most common for German DBF files)
                in_db = DBF(input_file, encoding='cp1252')
            except UnicodeDecodeError:
                try:
                    # Try iso-8859-1 (Latin-1, includes German characters)
                    in_db = DBF(input_file, encoding='iso-8859-1')
                except UnicodeDecodeError:
                    try:
                        # Try cp850 (DOS German codepage)
                        in_db = DBF(input_file, encoding='cp850')
                    except UnicodeDecodeError:
                        try:
                            # Try cp437 (original IBM PC codepage)
                            in_db = DBF(input_file, encoding='cp437')
                        except UnicodeDecodeError:
                            # Fallback to UTF-8
                            in_db = DBF(input_file, encoding='utf-8')
            
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
                        cleaned_values.append('')
                    elif isinstance(value, str):
                        # Replace line breaks with spaces and clean up other whitespace
                        cleaned_value = value.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                        # Remove multiple consecutive spaces
                        cleaned_value = ' '.join(cleaned_value.split())
                        # Remove any remaining problematic characters
                        cleaned_value = cleaned_value.replace('\x00', '').replace('\x1a', '')
                        cleaned_values.append(cleaned_value)
                    else:
                        cleaned_values.append(value)
                
                out_csv.writerow(cleaned_values)
                record_count += 1
                
                # Show progress every 1000 records
                if record_count % 1000 == 0:
                    print(f"Processed {record_count} records...")
            
            print(f"Conversion completed successfully! Processed {record_count} records.")
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
    parser = argparse.ArgumentParser(description='Convert DBF files to CSV format')
    parser.add_argument('input_file', help='Path to the input DBF file')
    parser.add_argument('-o', '--output', help='Path to the output CSV file (optional)')
    parser.add_argument('-d', '--delimiter', default=';', help='CSV delimiter (default: semicolon)')
    parser.add_argument('-e', '--encoding', default='utf-8', help='Output encoding (default: utf-8)')
    
    # Parse arguments
    args = parser.parse_args()
    success = convert_dbf_to_csv(args.input_file, args.output, args.delimiter, args.encoding)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()