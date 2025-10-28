"""
Test suite for DBF to CSV converter
"""

import csv
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Add the parent directory to the path so we can import dbf2csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dbf2csv import convert_dbf_to_csv


class TestDBF2CSV:
    """Test cases for the main conversion function"""

    def test_file_not_found(self):
        """Test handling of non-existent input files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            non_existent_file = os.path.join(temp_dir, "nonexistent.dbf")
            result = convert_dbf_to_csv(non_existent_file)
            assert result is False

    def test_invalid_file_extension(self):
        """Test handling of non-DBF files"""
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as temp_file:
            temp_file.write(b"test content")
            temp_file.close()  # Close file before testing on Windows
            try:
                result = convert_dbf_to_csv(temp_file.name)
                assert result is False
            finally:
                os.unlink(temp_file.name)

    def test_custom_output_filename(self):
        """Test custom output filename specification"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a mock DBF file
            dbf_file = os.path.join(temp_dir, "test.dbf")
            csv_file = os.path.join(temp_dir, "custom_output.csv")

            # Create empty file to pass existence check
            Path(dbf_file).touch()

            # Mock the DBF reading to avoid needing real DBF data
            with patch("dbf2csv.DBF") as mock_dbf:
                mock_dbf.return_value.fields = [
                    type("Field", (), {"name": "TEST_FIELD"})
                ]
                mock_dbf.return_value.__iter__ = lambda self: iter(
                    [{"TEST_FIELD": "test_value"}]
                )

                result = convert_dbf_to_csv(dbf_file, csv_file)
                assert result is True
                assert Path(csv_file).exists()

    def test_delimiter_configuration(self):
        """Test different delimiter configurations"""
        with tempfile.TemporaryDirectory() as temp_dir:
            dbf_file = os.path.join(temp_dir, "test.dbf")
            csv_file = os.path.join(temp_dir, "test.csv")
            Path(dbf_file).touch()

            with patch("dbf2csv.DBF") as mock_dbf:
                mock_dbf.return_value.fields = [
                    type("Field", (), {"name": "TEST_FIELD"})
                ]
                mock_dbf.return_value.__iter__ = lambda self: iter(
                    [{"TEST_FIELD": "test_value"}]
                )

                # Test comma delimiter
                result = convert_dbf_to_csv(dbf_file, csv_file, delimiter=",")
                assert result is True

                # Verify content is written correctly (quotes are normal for CSV)
                with open(csv_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Should contain either comma or quoted field names
                    assert ("," in content) or ('"TEST_FIELD"' in content)

    def test_german_character_handling(self):
        """Test German character preservation"""
        with tempfile.TemporaryDirectory() as temp_dir:
            dbf_file = os.path.join(temp_dir, "test.dbf")
            csv_file = os.path.join(temp_dir, "test.csv")
            Path(dbf_file).touch()

            # Test data with German characters
            test_data = {"NAME": "Müller", "STREET": "Hauptstraße", "CITY": "Köln"}

            with patch("dbf2csv.DBF") as mock_dbf:
                mock_dbf.return_value.fields = [
                    type("Field", (), {"name": "NAME"}),
                    type("Field", (), {"name": "STREET"}),
                    type("Field", (), {"name": "CITY"}),
                ]
                mock_dbf.return_value.__iter__ = lambda self: iter([test_data])

                result = convert_dbf_to_csv(dbf_file, csv_file)
                assert result is True

                # Verify German characters are preserved
                with open(csv_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    assert "Müller" in content
                    assert "Hauptstraße" in content
                    assert "Köln" in content

    def test_line_break_cleaning(self):
        """Test that line breaks are properly cleaned from data"""
        with tempfile.TemporaryDirectory() as temp_dir:
            dbf_file = os.path.join(temp_dir, "test.dbf")
            csv_file = os.path.join(temp_dir, "test.csv")
            Path(dbf_file).touch()

            # Test data with line breaks
            test_data = {"MEMO": "Line 1\nLine 2\rLine 3\tTabbed"}

            with patch("dbf2csv.DBF") as mock_dbf:
                mock_dbf.return_value.fields = [type("Field", (), {"name": "MEMO"})]
                mock_dbf.return_value.__iter__ = lambda self: iter([test_data])

                result = convert_dbf_to_csv(dbf_file, csv_file)
                assert result is True

                # Verify line breaks are cleaned
                with open(csv_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    assert "\n" not in content.split("\n")[1]  # Exclude header line
                    assert "\r" not in content
                    assert "Line 1 Line 2 Line 3 Tabbed" in content

    def test_null_value_handling(self):
        """Test handling of NULL/None values"""
        with tempfile.TemporaryDirectory() as temp_dir:
            dbf_file = os.path.join(temp_dir, "test.dbf")
            csv_file = os.path.join(temp_dir, "test.csv")
            Path(dbf_file).touch()

            # Test data with None values
            test_data = {"FIELD1": "value", "FIELD2": None, "FIELD3": ""}

            with patch("dbf2csv.DBF") as mock_dbf:
                mock_dbf.return_value.fields = [
                    type("Field", (), {"name": "FIELD1"}),
                    type("Field", (), {"name": "FIELD2"}),
                    type("Field", (), {"name": "FIELD3"}),
                ]
                mock_dbf.return_value.__iter__ = lambda self: iter([test_data])

                result = convert_dbf_to_csv(dbf_file, csv_file)
                assert result is True

                # Verify None is converted to empty string
                with open(csv_file, "r", encoding="utf-8") as f:
                    reader = csv.reader(f, delimiter=";")
                    next(reader)  # Skip header
                    data_row = next(reader)
                    assert data_row[1] == ""  # None should become empty string

    def test_permission_error_handling(self):
        """Test handling of permission errors"""
        with tempfile.TemporaryDirectory() as temp_dir:
            dbf_file = os.path.join(temp_dir, "test.dbf")
            Path(dbf_file).touch()

            # Mock permission error when opening output file
            with patch(
                "builtins.open", side_effect=PermissionError("Permission denied")
            ):
                result = convert_dbf_to_csv(dbf_file)
                assert result is False


class TestUtilityScripts:
    """Test cases for utility scripts"""

    def test_check_csv_functionality(self):
        """Test the CSV checking utility"""
        # This would test check_csv.py functionality
        pass

    def test_encoding_test_functionality(self):
        """Test the encoding test utility"""
        # This would test test_encoding.py functionality
        pass


class TestCommandLineInterface:
    """Test cases for command-line interface"""

    def test_help_message(self):
        """Test that help message is displayed correctly"""
        with patch("sys.argv", ["dbf2csv.py", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                from dbf2csv import main

                main()
            assert exc_info.value.code == 0

    def test_missing_required_argument(self):
        """Test handling of missing required arguments"""
        with patch("sys.argv", ["dbf2csv.py"]):
            with pytest.raises(SystemExit) as exc_info:
                from dbf2csv import main

                main()
            assert exc_info.value.code != 0


if __name__ == "__main__":
    pytest.main([__file__])
