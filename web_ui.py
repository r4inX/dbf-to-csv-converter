#!/usr/bin/env python3
"""
Flask Web UI for DBF to CSV Converter
A simple web interface for converting DBF files to CSV
"""

import os
import tempfile
import uuid
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
import dbf2csv

app = Flask(__name__)
app.secret_key = 'dbf-converter-secret-key-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Create uploads directory
UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'dbf'}

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_dbf_info(dbf_path):
    """Extract metadata from DBF file"""
    try:
        from dbfread import DBF
        
        # Try different encodings to get basic info
        for encoding in ['cp1252', 'iso-8859-1', 'cp850', 'cp437', 'utf-8']:
            try:
                with DBF(dbf_path, encoding=encoding) as dbf:
                    info = {
                        'filename': Path(dbf_path).name,
                        'record_count': len(dbf),
                        'field_count': len(dbf.fields),
                        'fields': [{'name': field.name, 'type': field.type, 'length': field.length} 
                                 for field in dbf.fields],
                        'encoding_used': encoding,
                        'file_size': Path(dbf_path).stat().st_size,
                    }
                    
                    # Get sample of first few records
                    sample_records = []
                    for i, record in enumerate(dbf):
                        if i >= 3:  # Only first 3 records
                            break
                        sample_records.append(dict(record))
                    
                    info['sample_records'] = sample_records
                    return info
                    
            except Exception:
                continue
                
        return {'error': 'Could not read DBF file with any supported encoding'}
        
    except Exception as e:
        return {'error': f'Error reading DBF file: {str(e)}'}

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and show preview"""
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        session_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_path = app.config['UPLOAD_FOLDER'] / f"{session_id}_{filename}"
        
        file.save(file_path)
        
        # Get DBF info for preview
        dbf_info = get_dbf_info(file_path)
        
        return render_template('preview.html', 
                             dbf_info=dbf_info, 
                             session_id=session_id,
                             original_filename=filename)
    else:
        flash('Invalid file type. Please upload a .dbf file.')
        return redirect(url_for('index'))

@app.route('/convert', methods=['POST'])
def convert_file():
    """Convert DBF file to CSV with user-specified options"""
    try:
        session_id = request.form.get('session_id')
        original_filename = request.form.get('original_filename')
        delimiter = request.form.get('delimiter', ';')
        encoding = request.form.get('encoding', 'utf-8')
        
        if not session_id or not original_filename:
            return jsonify({'error': 'Missing session information'}), 400
        
        # Find uploaded file
        dbf_path = None
        for file_path in app.config['UPLOAD_FOLDER'].glob(f"{session_id}_*"):
            if file_path.name.endswith(original_filename):
                dbf_path = file_path
                break
        
        if not dbf_path or not dbf_path.exists():
            return jsonify({'error': 'Original file not found'}), 404
        
        # Create output filename
        csv_filename = f"{Path(original_filename).stem}.csv"
        csv_path = app.config['UPLOAD_FOLDER'] / f"{session_id}_{csv_filename}"
        
        # Convert file
        success = dbf2csv.convert_dbf_to_csv(
            str(dbf_path), 
            str(csv_path), 
            delimiter=delimiter, 
            encoding=encoding
        )
        
        if success:
            return jsonify({
                'success': True,
                'download_url': url_for('download_file', 
                                      session_id=session_id, 
                                      filename=csv_filename)
            })
        else:
            return jsonify({'error': 'Conversion failed'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Conversion error: {str(e)}'}), 500

@app.route('/download/<session_id>/<filename>')
def download_file(session_id, filename):
    """Download converted CSV file"""
    try:
        file_path = app.config['UPLOAD_FOLDER'] / f"{session_id}_{filename}"
        
        if not file_path.exists():
            flash('File not found or expired')
            return redirect(url_for('index'))
        
        return send_file(file_path, 
                        as_attachment=True, 
                        download_name=filename,
                        mimetype='text/csv')
        
    except Exception as e:
        flash(f'Download error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/cleanup/<session_id>')
def cleanup_files(session_id):
    """Clean up temporary files"""
    try:
        for file_path in app.config['UPLOAD_FOLDER'].glob(f"{session_id}_*"):
            file_path.unlink()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)