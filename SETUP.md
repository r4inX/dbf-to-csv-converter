# Setup Guide for GitHub

## Files to include in your repository:

✅ **Core files:**
- `dbf2csv.py` - Main conversion script
- `requirements.txt` - Python dependencies
- `README.md` - Documentation
- `LICENSE` - MIT license
- `.gitignore` - Git ignore rules

✅ **Utility scripts:**
- `check_csv.py` - Verify German character encoding
- `test_encoding.py` - Test different DBF encodings

## Files to exclude:
❌ Your actual DBF data files (DAT_COVER_28102025/) - these contain personal/business data
❌ Large CSV output files - keep only small demo files

## GitHub commands:

```bash
# Initialize repository
git init
git add .
git commit -m "Initial commit: DBF to CSV converter with German character support"

# Connect to GitHub (replace with your repository URL)
git remote add origin https://github.com/yourusername/dbf-to-csv-converter.git
git branch -M main
git push -u origin main
```

## Repository structure:
```
dbf-to-csv-converter/
├── dbf2csv.py              # Main script
├── check_csv.py            # Verification utility
├── test_encoding.py        # Encoding test utility
├── requirements.txt        # Dependencies
├── README.md               # Documentation
├── LICENSE                 # MIT license
└── .gitignore             # Git ignore rules
```