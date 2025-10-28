# DBF to CSV Converter

[![CI](https://github.com/r4inX/dbf-to-csv-converter/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/r4inX/dbf-to-csv-converter/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub release](https://img.shields.io/github/v/release/r4inX/dbf-to-csv-converter.svg)](https://github.com/r4inX/dbf-to-csv-converter/releases)
[![GitHub stars](https://img.shields.io/github/stars/r4inX/dbf-to-csv-converter.svg?style=social)](https://github.com/r4inX/dbf-to-csv-converter)

A robust Python script to convert DBF (dBASE) files to CSV format with proper handling of German characters and special formatting requirements.

## 🚀 Quick Start

### Option 1: Web Interface (Recommended)
```bash
pip install flask werkzeug dbfread
python web_ui.py
# Open http://localhost:5000 in your browser
```

### Option 2: Command Line
```bash
pip install dbfread
python dbf2csv.py your_file.dbf
```

## Features

### 🌐 **Web Interface**
- **Drag & drop upload** - Easy file selection with visual feedback
- **Real-time preview** - See your data structure before conversion
- **Smart options** - Automatic encoding detection with manual override
- **Progress tracking** - Visual progress bar during conversion
- **One-click download** - Instant CSV file download

### 🖥️ **Command Line**
- **Multiple encoding support** - Automatically detects and handles various character encodings (cp1252, iso-8859-1, cp850, etc.)
- **German character support** - Properly converts German umlauts (ä, ö, ü, ß) and special characters
- **Configurable delimiters** - Choose between semicolon (`;`) or comma (`,`) delimiters
- **Data cleaning** - Removes line breaks and problematic characters from memo fields
- **Progress tracking** - Shows conversion progress for large files
- **Error handling** - Comprehensive error handling with clear error messages

## Requirements

- Python 3.6+
- `dbfread` library

## Installation

1. Clone this repository:
```bash
git clone https://github.com/r4inX/dbf-to-csv-converter/dbf-to-csv-converter.git
cd dbf-to-csv-converter
```

2. Install required dependencies:
```bash
pip install dbfread
```

## Usage

### Basic Usage

Convert a DBF file to CSV with default settings (semicolon delimiter):

```bash
python dbf2csv.py input_file.dbf
```

### Advanced Usage

```bash
# Custom output file
python dbf2csv.py input_file.dbf -o output_file.csv

# Use comma delimiter (Excel-friendly)
python dbf2csv.py input_file.dbf -d ","

# Custom encoding
python dbf2csv.py input_file.dbf -e "utf-8"

# Combine options
python dbf2csv.py input_file.dbf -o addresses.csv -d "," -e "utf-8"

# Get help
python dbf2csv.py --help
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `input_file` | Path to input DBF file | Required |
| `-o, --output` | Output CSV file path | `input_file.csv` |
| `-d, --delimiter` | CSV field delimiter | `;` (semicolon) |
| `-e, --encoding` | Output file encoding | `utf-8` |
| `-h, --help` | Show help message | - |

## Example Usage

### Basic Conversion
```bash
python dbf2csv.py your_table.dbf
```

**Expected Output:**
```
Converting 'your_table.dbf' to 'your_table.csv'
Processed 1000 records...
Processed 2000 records...
Conversion completed successfully! Processed 2350 records.
```

### Sample Output Format
The converter produces clean, properly formatted CSV files:

```csv
"ID";"NAME";"ADDRESS";"CITY";"POSTAL_CODE"
"1";"Max Müller";"Hauptstraße 123";"München";"80331"
"2";"Anna Schöne";"Goethestraße 45";"Köln";"50674"
"3";"Klaus Größer";"Bahnhofstraße 78";"Düsseldorf";"40210"
```

Notice how German characters (ü, ö, ß) are properly preserved in the output.

## Utility Scripts

### check_csv.py
Verify that German characters are properly encoded in the converted CSV files:

```bash
python check_csv.py output_file.csv
```

This script will scan the CSV file and display any German text found, helping you verify the encoding worked correctly.

### test_encoding.py
Test different character encodings on a DBF file to determine the best encoding:

```bash
python test_encoding.py input_file.dbf
```

## Character Encoding

The script automatically tries multiple encoding methods in this order:

1. **cp1252** - Windows German codepage (most common)
2. **iso-8859-1** - Latin-1 (includes German characters)
3. **cp850** - DOS German codepage
4. **cp437** - Original IBM PC codepage
5. **utf-8** - Fallback encoding

This ensures maximum compatibility with DBF files created by different systems.

## Error Handling

The script includes comprehensive error handling for:

- **File not found** - Clear error when input file doesn't exist
- **Invalid file type** - Validates that input is actually a DBF file
- **Permission errors** - Handles read/write permission issues
- **Encoding errors** - Tries multiple encodings automatically
- **Data corruption** - Cleans problematic characters and formatting

## Data Cleaning Features

- **Line break removal** - Converts `\n`, `\r`, `\t` to spaces
- **Whitespace normalization** - Removes excessive spaces
- **Control character removal** - Removes `\x00`, `\x1a` characters
- **NULL value handling** - Converts None values to empty strings
- **Quote protection** - All fields are properly quoted to prevent CSV parsing issues

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

**Q: German characters appear corrupted in PowerShell**
A: This is a PowerShell display issue. The actual CSV file contains correctly encoded characters. Open the file in Excel, Notepad++, or VS Code to verify.

**Q: Some fields contain unexpected characters**
A: Run the `test_encoding.py` script to determine if a different encoding would work better for your specific DBF file.

**Q: CSV import fails in Excel**
A: Try using comma delimiter (`-d ","`) for better Excel compatibility.

**Q: Large files take too long**
A: The script shows progress every 1000 records. For very large files, this is normal behavior.

## Performance

- **Small files** (< 1000 records): Near-instant conversion
- **Medium files** (1000-10000 records): 1-5 seconds
- **Large files** (> 10000 records): Progress indicator shows every 1000 records

## Acknowledgments

- Built with the excellent [`dbfread`](https://github.com/olemb/dbfread) library
- Inspired by the need for reliable German character handling in legacy database conversions
- Thanks to the open-source community for DBF format documentation

---

## Project Stats

![GitHub repo size](https://img.shields.io/github/repo-size/r4inX/dbf-to-csv-converter)
![GitHub code size](https://img.shields.io/github/languages/code-size/r4inX/dbf-to-csv-converter)
![GitHub last commit](https://img.shields.io/github/last-commit/r4inX/dbf-to-csv-converter)

## Support

- **Documentation**: You're reading it!
- **Bug Reports**: [Create an issue](https://github.com/r4inX/dbf-to-csv-converter/issues)
- **Feature Requests**: [Start a discussion](https://github.com/r4inX/dbf-to-csv-converter/discussions)
- **Show Support**: Give this repo a star if it helped you!

---

**Made with ❤️ for the open-source community**

If this tool helped you, please consider giving it a star ⭐ on GitHub!
