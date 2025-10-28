---
layout: default
title: Home
---

<div class="hero-section" style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; margin: -2rem -2rem 2rem -2rem; border-radius: 0 0 1rem 1rem;">
  <h1 style="font-size: 2.5rem; margin-bottom: 1rem; color: white;">🔄 DBF to CSV Converter</h1>
  <p style="font-size: 1.2rem; margin-bottom: 1.5rem; opacity: 0.9;">Convert DBF files to CSV with perfect German character support</p>
  <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
    <a href="https://github.com/r4inX/dbf-to-csv-converter" class="btn btn-primary" style="background: white; color: #667eea; padding: 0.75rem 1.5rem; border-radius: 0.5rem; text-decoration: none; font-weight: bold; display: inline-block;">📁 View on GitHub</a>
    <a href="https://github.com/r4inX/dbf-to-csv-converter/releases" class="btn btn-secondary" style="background: rgba(255,255,255,0.2); color: white; padding: 0.75rem 1.5rem; border-radius: 0.5rem; text-decoration: none; font-weight: bold; display: inline-block;">📦 Download Latest</a>
  </div>
</div>

## ✨ Why Choose This Converter?

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0;">
  <div style="padding: 1.5rem; border: 1px solid #e1e5e9; border-radius: 0.5rem; background: #f8f9fa;">
    <h3 style="color: #2196F3; margin-top: 0;">🌍 German Character Support</h3>
    <p>Perfect handling of German umlauts (ä, ö, ü, ß) and special characters. No more corrupted text!</p>
  </div>
  
  <div style="padding: 1.5rem; border: 1px solid #e1e5e9; border-radius: 0.5rem; background: #f8f9fa;">
    <h3 style="color: #4CAF50; margin-top: 0;">🔧 Smart Encoding Detection</h3>
    <p>Automatically detects the best encoding from cp1252, iso-8859-1, cp850, cp437, and utf-8.</p>
  </div>
  
  <div style="padding: 1.5rem; border: 1px solid #e1e5e9; border-radius: 0.5rem; background: #f8f9fa;">
    <h3 style="color: #FF9800; margin-top: 0;">🧹 Data Cleaning</h3>
    <p>Removes line breaks, normalizes whitespace, and handles problematic characters automatically.</p>
  </div>
  
  <div style="padding: 1.5rem; border: 1px solid #e1e5e9; border-radius: 0.5rem; background: #f8f9fa;">
    <h3 style="color: #9C27B0; margin-top: 0;">⚡ Fast & Reliable</h3>
    <p>Processes thousands of records quickly with progress tracking and comprehensive error handling.</p>
  </div>
</div>

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/r4inX/dbf-to-csv-converter.git
cd dbf-to-csv-converter

# Install dependencies
pip install -r requirements.txt

# Convert your DBF file
python dbf2csv.py your_file.dbf
```

## 📊 Supported Features

| Feature | Status | Description |
|---------|---------|-------------|
| German Characters | ✅ | Perfect ä, ö, ü, ß support |
| Multiple Encodings | ✅ | Auto-detection of cp1252, iso-8859-1, cp850, cp437, utf-8 |
| Custom Delimiters | ✅ | Semicolon or comma separators |
| Data Cleaning | ✅ | Line break removal, whitespace normalization |
| Progress Tracking | ✅ | Real-time progress for large files |
| Error Handling | ✅ | Comprehensive error messages |
| Command Line | ✅ | Professional CLI with help |

## 🎯 Perfect For

- **Legacy Database Migration** - Convert old dBASE files to modern CSV format
- **German Business Data** - Preserve German characters in customer/address databases  
- **Data Processing Pipelines** - Reliable batch conversion of DBF files
- **Excel Integration** - Create Excel-compatible CSV files with proper encoding

## 🏆 Quality Assurance

[![CI](https://github.com/r4inX/dbf-to-csv-converter/workflows/CI%2FCD%20Pipeline/badge.svg)](https://github.com/r4inX/dbf-to-csv-converter/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

- **Automated Testing** - Tests on Python 3.8-3.12 across Ubuntu, Windows, and macOS
- **Code Quality** - Black formatting, flake8 linting, security scanning
- **Open Source** - MIT licensed, community-driven development

---

<div style="text-align: center; margin: 3rem 0; padding: 2rem; background: #f8f9fa; border-radius: 0.5rem;">
  <h2 style="color: #333; margin-bottom: 1rem;">Ready to Convert Your DBF Files?</h2>
  <p style="font-size: 1.1rem; margin-bottom: 1.5rem; color: #666;">Join hundreds of users who trust this tool for their data conversion needs.</p>
  <a href="https://github.com/r4inX/dbf-to-csv-converter" style="background: #667eea; color: white; padding: 1rem 2rem; border-radius: 0.5rem; text-decoration: none; font-weight: bold; font-size: 1.1rem;">Get Started Now →</a>
</div>