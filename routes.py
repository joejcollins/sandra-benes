import os
import json
import csv
import mimetypes
from flask import render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from app import app
from utils import get_file_type, validate_file, read_file_content, write_file_content, get_file_list

@app.route('/')
def index():
    """Main page showing list of data files"""
    search_query = request.args.get('search', '').lower()
    file_type_filter = request.args.get('type', '')
    
    try:
        files = get_file_list(app.config['DATA_FOLDER'])
        
        # Apply filters
        if search_query:
            files = [f for f in files if search_query in f['name'].lower()]
        
        if file_type_filter:
            files = [f for f in files if f['type'] == file_type_filter]
        
        # Get unique file types for filter dropdown
        all_files = get_file_list(app.config['DATA_FOLDER'])
        file_types = list(set(f['type'] for f in all_files))
        
        return render_template('index.html', 
                             files=files, 
                             search_query=search_query,
                             file_type_filter=file_type_filter,
                             file_types=file_types)
    except Exception as e:
        app.logger.error(f"Error loading file list: {str(e)}")
        flash(f"Error loading files: {str(e)}", 'error')
        return render_template('index.html', files=[], file_types=[], search_query='', file_type_filter='')

@app.route('/view/<filename>')
def view_file(filename):
    """View a specific file with proper formatting"""
    try:
        file_path = os.path.join(app.config['DATA_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(file_path):
            flash(f"File '{filename}' not found.", 'error')
            return redirect(url_for('index'))
        
        file_info = {
            'name': filename,
            'type': get_file_type(filename),
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path)
        }
        
        content, error = read_file_content(file_path, file_info['type'])
        
        if error:
            flash(f"Error reading file: {error}", 'error')
            return redirect(url_for('index'))
        
        return render_template('view_file.html', 
                             file_info=file_info, 
                             content=content)
    except Exception as e:
        app.logger.error(f"Error viewing file {filename}: {str(e)}")
        flash(f"Error viewing file: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/edit/<filename>')
def edit_file(filename):
    """Edit a specific file"""
    try:
        file_path = os.path.join(app.config['DATA_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(file_path):
            flash(f"File '{filename}' not found.", 'error')
            return redirect(url_for('index'))
        
        file_info = {
            'name': filename,
            'type': get_file_type(filename),
            'size': os.path.getsize(file_path),
            'modified': os.path.getmtime(file_path)
        }
        
        # For editing, we always want the raw content
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        return render_template('edit_file.html', 
                             file_info=file_info, 
                             content=raw_content)
    except Exception as e:
        app.logger.error(f"Error editing file {filename}: {str(e)}")
        flash(f"Error opening file for editing: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/save/<filename>', methods=['POST'])
def save_file(filename):
    """Save changes to a file"""
    try:
        file_path = os.path.join(app.config['DATA_FOLDER'], secure_filename(filename))
        content = request.form.get('content', '')
        
        # Validate file content based on type
        file_type = get_file_type(filename)
        validation_error = validate_file(content, file_type)
        
        if validation_error:
            flash(f"Validation error: {validation_error}", 'error')
            return redirect(url_for('edit_file', filename=filename))
        
        # Write content to file
        error = write_file_content(file_path, content, file_type)
        
        if error:
            flash(f"Error saving file: {error}", 'error')
            return redirect(url_for('edit_file', filename=filename))
        
        flash(f"File '{filename}' saved successfully!", 'success')
        return redirect(url_for('view_file', filename=filename))
        
    except Exception as e:
        app.logger.error(f"Error saving file {filename}: {str(e)}")
        flash(f"Error saving file: {str(e)}", 'error')
        return redirect(url_for('edit_file', filename=filename))

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            flash('No file selected for upload.', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected for upload.', 'error')
            return redirect(url_for('index'))
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['DATA_FOLDER'], filename)
            
            # Check if file already exists
            if os.path.exists(file_path):
                flash(f"File '{filename}' already exists. Please rename or delete the existing file first.", 'error')
                return redirect(url_for('index'))
            
            # Validate file type
            file_type = get_file_type(filename)
            if file_type == 'unsupported':
                flash('Unsupported file type. Please upload CSV, JSON, or text files only.', 'error')
                return redirect(url_for('index'))
            
            # Save file
            file.save(file_path)
            
            # Validate file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            validation_error = validate_file(content, file_type)
            if validation_error:
                os.remove(file_path)  # Remove invalid file
                flash(f"Invalid file content: {validation_error}", 'error')
                return redirect(url_for('index'))
            
            flash(f"File '{filename}' uploaded successfully!", 'success')
            return redirect(url_for('view_file', filename=filename))
    
    except Exception as e:
        app.logger.error(f"Error uploading file: {str(e)}")
        flash(f"Error uploading file: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    """Delete a file"""
    try:
        file_path = os.path.join(app.config['DATA_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(file_path):
            flash(f"File '{filename}' not found.", 'error')
            return redirect(url_for('index'))
        
        os.remove(file_path)
        flash(f"File '{filename}' deleted successfully!", 'success')
        return redirect(url_for('index'))
        
    except Exception as e:
        app.logger.error(f"Error deleting file {filename}: {str(e)}")
        flash(f"Error deleting file: {str(e)}", 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Download a file"""
    try:
        return send_from_directory(app.config['DATA_FOLDER'], 
                                 secure_filename(filename), 
                                 as_attachment=True)
    except Exception as e:
        app.logger.error(f"Error downloading file {filename}: {str(e)}")
        flash(f"Error downloading file: {str(e)}", 'error')
        return redirect(url_for('index'))
