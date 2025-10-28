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

ALLOWED_EXTENSIONS = {'dbf', 'fpt', 'cdx', 'dbt'}

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_companion_files(dbf_path):
    """Find and copy companion files (.fpt, .cdx, .dbt) for a DBF file"""
    base_path = Path(dbf_path).parent
    base_name = Path(dbf_path).stem
    
    companion_files = []
    
    # First, check if companion files were already uploaded with the same session ID
    session_id = base_name.split('_')[0]
    dbf_name = '_'.join(base_name.split('_')[1:])  # Remove session prefix
    
    for ext in ['.FPT', '.fpt', '.CDX', '.cdx', '.DBT', '.dbt']:
        # Check if already uploaded
        uploaded_companion = base_path / f"{session_id}_{dbf_name}{ext}"
        if uploaded_companion.exists():
            companion_files.append(uploaded_companion)
            print(f"Found uploaded companion file: {uploaded_companion}")
            continue
            
        # Look for companion files in common directories
        potential_dirs = [
            Path('.'),  # Current directory
            Path('DAT_COVER_28102025'),  # Specific directory if it exists
            base_path.parent,  # Parent of uploads directory
        ]
        
        for source_dir in potential_dirs:
            if source_dir.exists():
                # Try exact name match
                source_file = source_dir / f"{dbf_name}{ext}"
                if source_file.exists():
                    # Copy to uploads directory with session prefix
                    dest_file = base_path / f"{session_id}_{dbf_name}{ext}"
                    try:
                        import shutil
                        shutil.copy2(source_file, dest_file)
                        companion_files.append(dest_file)
                        print(f"Copied companion file: {source_file} -> {dest_file}")
                        break  # Found it, don't check other directories
                    except Exception as e:
                        print(f"Failed to copy {source_file}: {e}")
    
    return companion_files

def get_dbf_info(dbf_path):
    """Extract metadata from DBF file"""
    try:
        from dbfread import DBF
        
        # First, try to find and copy companion files
        companion_files = find_companion_files(dbf_path)
        if companion_files:
            print(f"Found companion files: {[str(f) for f in companion_files]}")
        
        # Try different encodings to get basic info
        encodings_to_try = ['cp1252', 'iso-8859-1', 'cp850', 'cp437', 'utf-8', 'latin1']
        
        last_error = None
        for encoding in encodings_to_try:
            try:
                print(f"Trying encoding: {encoding}")
                dbf = DBF(dbf_path, encoding=encoding, char_decode_errors='ignore')
                
                # Try to get record count safely
                try:
                    record_count = len(dbf)
                except:
                    # If len() fails, count manually
                    record_count = 0
                    try:
                        for _ in dbf:
                            record_count += 1
                        dbf = DBF(dbf_path, encoding=encoding, char_decode_errors='ignore')  # Reopen after counting
                    except Exception as count_error:
                        print(f"Could not count records with {encoding}: {count_error}")
                        continue
                
                info = {
                    'filename': Path(dbf_path).name,
                    'record_count': record_count,
                    'field_count': len(dbf.fields),
                    'fields': [{'name': field.name, 'type': field.type, 'length': field.length} 
                             for field in dbf.fields],
                    'encoding_used': encoding,
                    'file_size': Path(dbf_path).stat().st_size,
                    'companion_files': [f.name for f in companion_files] if companion_files else []
                }
                
                # Get sample of first few records with safe data conversion
                sample_records = []
                try:
                    record_iter = iter(dbf)
                    for i in range(min(3, record_count)):  # Only first 3 records or less
                        try:
                            record = next(record_iter)
                            
                            # Convert all values to strings to avoid template errors
                            safe_record = {}
                            for key, value in record.items():
                                if value is None:
                                    safe_record[key] = ''
                                elif isinstance(value, (int, float)):
                                    safe_record[key] = str(value)
                                elif isinstance(value, bytes):
                                    try:
                                        safe_record[key] = value.decode(encoding, errors='replace')
                                    except:
                                        safe_record[key] = str(value)
                                else:
                                    safe_record[key] = str(value)
                            
                            sample_records.append(safe_record)
                        except StopIteration:
                            break
                        except Exception as record_error:
                            print(f"Error reading record {i}: {record_error}")
                            continue
                            
                except Exception as e:
                    # If we can't read records, at least we have the structure
                    info['sample_error'] = f"Could not read sample data: {str(e)}"
                    print(f"Sample data error with {encoding}: {e}")
                
                info['sample_records'] = sample_records
                print(f"Successfully read DBF with encoding: {encoding}")
                return info
                    
            except Exception as e:
                last_error = e
                print(f"Failed with encoding {encoding}: {str(e)}")
                continue
        
        # If all encodings failed, provide helpful error message
        try:
            file_size = Path(dbf_path).stat().st_size
            error_msg = f'Could not read DBF file with any supported encoding. File size: {file_size} bytes.'
            
            if 'memo' in str(last_error).lower():
                error_msg += f' This DBF file requires memo files (.FPT). Please upload both the .DBF and .FPT files, or use the command line tool in the same directory as your files.'
            else:
                error_msg += f' Last error: {str(last_error)}. Try using the command line tool.'
                
            return {
                'error': error_msg,
                'filename': Path(dbf_path).name,
                'file_size': file_size
            }
        except Exception:
            return {'error': f'Could not read DBF file - file may be corrupted or not a valid DBF file. Last error: {str(last_error)}'}
        
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
    
    files = request.files.getlist('file')
    if not files or all(f.filename == '' for f in files):
        flash('No files selected')
        return redirect(request.url)
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    # Find the main DBF file and companion files
    dbf_file = None
    companion_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = app.config['UPLOAD_FOLDER'] / f"{session_id}_{filename}"
            file.save(file_path)
            
            if filename.lower().endswith('.dbf'):
                dbf_file = file_path
                original_filename = filename
            else:
                companion_files.append(file_path)
    
    if not dbf_file:
        flash('Please upload a .DBF file')
        return redirect(url_for('index'))
    
    # Get DBF info for preview
    dbf_info = get_dbf_info(dbf_file)
    
    # Add info about uploaded companion files
    if companion_files:
        uploaded_companions = [f.name.split('_', 1)[1] for f in companion_files]  # Remove session prefix
        if 'companion_files' not in dbf_info:
            dbf_info['companion_files'] = []
        dbf_info['companion_files'].extend(uploaded_companions)
        dbf_info['uploaded_companions'] = uploaded_companions
    
    return render_template('preview.html', 
                         dbf_info=dbf_info, 
                         session_id=session_id,
                         original_filename=original_filename)

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