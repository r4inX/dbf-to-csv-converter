#!/usr/bin/python

import sys

from dbfread import DBF


def test_encodings(dbf_file):
    """Test different encodings to find the correct one for German characters"""

    encodings_to_test = [
        "cp850",  # DOS German
        "cp1252",  # Windows German
        "iso-8859-1",  # Latin-1
        "iso-8859-15",  # Latin-9 (includes Euro symbol)
        "cp437",  # Original IBM PC
        "utf-8",  # UTF-8
        "latin1",  # alias for iso-8859-1
    ]

    print(f"Testing encodings for: {dbf_file}")
    print("=" * 50)

    for encoding in encodings_to_test:
        try:
            print(f"\nTesting encoding: {encoding}")
            in_db = DBF(dbf_file, encoding=encoding)

            # Get first few records to test
            count = 0
            for rec in in_db:
                count += 1
                # Look for a record with German characters
                for field_name, value in rec.items():
                    if isinstance(value, str) and any(
                        char in value.lower()
                        for char in ["ä", "ö", "ü", "ß", "straße", "für", "mühl"]
                    ):
                        print(f"  Found German text in {field_name}: {value}")
                        break
                if count >= 10:  # Only check first 10 records
                    break

        except Exception as e:
            print(f"  Error with {encoding}: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        test_encodings(sys.argv[1])
    else:
        print("Usage: python test_encoding.py <dbf_file>")
