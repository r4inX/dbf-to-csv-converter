#!/usr/bin/env python3
"""Quick test of the data validator module"""

from dbfread import DBF

from data_validator import DBFDataValidator


def test_validator():
    print("✅ Data validator import successful")

    # Read DBF file properly
    dbf_file = "DAT_COVER_28102025/T_ANREDE.dbf"

    for encoding in ["cp1252", "iso-8859-1", "cp850", "cp437", "utf-8"]:
        try:
            dbf = DBF(dbf_file, encoding=encoding, char_decode_errors="ignore")
            records = list(dbf)
            field_info = [
                {"name": f.name, "type": f.type, "length": f.length} for f in dbf.fields
            ]

            # Test with correct parameters
            validator = DBFDataValidator(records, field_info, encoding)
            results = validator.run_full_validation()

            print(f"Quality Score: {results['quality_score']['overall_score']:.1f}")
            print(f"Grade: {results['summary']['overall_quality']}")
            print(f"Duplicates: {results['duplicates']['total_duplicates']}")
            print(f"Encoding: {results['encoding_confidence']['confidence_level']}")
            print("✅ Data validation working correctly")
            break

        except Exception as e:
            print(f"Failed with encoding {encoding}: {e}")
            continue


if __name__ == "__main__":
    test_validator()
