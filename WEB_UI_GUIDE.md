# 🌐 Web UI Usage Guide

## Quick Start

1. **Start the web interface:**
   ```bash
   python web_ui.py
   ```

2. **Open your browser:** 
   Navigate to `http://localhost:5000`

3. **Upload & Convert:**
   - Drag & drop your DBF file or click to browse
   - Preview file contents and structure
   - Configure conversion options
   - Download your CSV file

## Features

### 📂 **Easy File Upload**
- Drag & drop interface
- File validation (DBF files only)
- Size limit: 50MB
- Instant file information display

### 👀 **Smart Preview**
- Record count and field analysis
- Data type detection
- Sample data preview (first 3 records)
- Encoding detection results

### ⚙️ **Conversion Options**
- **Delimiters:** Semicolon (German), Comma (International), Pipe, Tab
- **Encoding:** UTF-8, Windows-1252, ISO-8859-1
- **Real-time progress** tracking
- **One-click download** of results

### 🔧 **Advanced Features**
- Automatic encoding detection
- German character preservation
- Data cleaning and validation
- Temporary file cleanup
- Mobile-responsive design

## Screenshots

The web interface provides:
- 🎨 Beautiful gradient design
- 📱 Mobile-friendly responsive layout
- 🌍 German character support indicators
- ⚡ Real-time conversion progress
- 🗂️ Detailed file structure preview

## Technical Details

### File Handling
- Files are temporarily stored in `uploads/` directory
- Unique session IDs prevent conflicts
- Automatic cleanup after download
- Secure filename handling

### Supported Encodings
- **cp1252** (Windows German) - Primary
- **iso-8859-1** (Latin-1) - Fallback
- **cp850** (DOS German) - Legacy
- **cp437** (DOS US) - Compatibility
- **utf-8** - Modern standard

### Browser Compatibility
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers supported

## Security Notes

- 50MB file size limit
- Temporary file cleanup
- Secure filename validation
- Local processing only
- No data transmitted externally

## Troubleshooting

### Common Issues

**Web interface won't start:**
```bash
pip install flask werkzeug
python web_ui.py
```

**File upload fails:**
- Check file is .DBF format
- Ensure file size < 50MB
- Try refreshing the page

**Conversion errors:**
- File may be corrupted
- Try different encoding in preview
- Check original DBF file

### Port Conflicts
If port 5000 is busy, edit `web_ui.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Production Deployment

For production use, consider:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_ui:app
```

Or with Docker:
```dockerfile
FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "web_ui:app"]
```