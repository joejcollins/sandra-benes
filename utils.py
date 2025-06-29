import os
import json
import csv
import io
from datetime import datetime

def get_file_type(filename):
    """Determine file type based on extension"""
    ext = os.path.splitext(filename)[1].lower()
    if ext == '.csv':
        return 'csv'
    elif ext == '.json':
        return 'json'
    elif ext in ['.txt', '.md', '.log']:
        return 'text'
    else:
        return 'unsupported'

def get_file_list(data_folder):
    """Get list of all supported files in the data folder"""
    files = []
    
    if not os.path.exists(data_folder):
        return files
    
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        
        if os.path.isfile(file_path):
            file_type = get_file_type(filename)
            
            if file_type != 'unsupported':
                stat = os.stat(file_path)
                files.append({
                    'name': filename,
                    'type': file_type,
                    'size': stat.st_size,
                    'modified': datetime.fromtimestamp(stat.st_mtime),
                    'size_formatted': format_file_size(stat.st_size)
                })
    
    # Sort by name
    files.sort(key=lambda x: x['name'].lower())
    return files

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"

def read_file_content(file_path, file_type):
    """Read and format file content based on type"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
        
        if file_type == 'csv':
            return format_csv_content(raw_content), None
        elif file_type == 'json':
            return format_json_content(raw_content), None
        else:  # text
            return raw_content, None
            
    except Exception as e:
        return None, str(e)

def format_csv_content(content):
    """Format CSV content for display"""
    try:
        # Parse CSV and return as structured data
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        
        if not rows:
            return {"type": "csv", "headers": [], "rows": []}
        
        headers = rows[0] if rows else []
        data_rows = rows[1:] if len(rows) > 1 else []
        
        return {
            "type": "csv",
            "headers": headers,
            "rows": data_rows,
            "raw": content
        }
    except Exception:
        # If parsing fails, return as raw text
        return {"type": "text", "content": content}

def format_json_content(content):
    """Format JSON content for display"""
    try:
        parsed = json.loads(content)
        formatted = json.dumps(parsed, indent=2, ensure_ascii=False)
        return {
            "type": "json",
            "formatted": formatted,
            "parsed": parsed,
            "raw": content
        }
    except Exception:
        # If parsing fails, return as raw text
        return {"type": "text", "content": content}

def validate_file(content, file_type):
    """Validate file content based on type"""
    try:
        if file_type == 'csv':
            # Try to parse CSV
            reader = csv.reader(io.StringIO(content))
            list(reader)  # This will raise an exception if invalid
            return None
        elif file_type == 'json':
            # Try to parse JSON
            json.loads(content)
            return None
        else:  # text files don't need validation
            return None
    except csv.Error as e:
        return f"Invalid CSV format: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Invalid JSON format: {str(e)}"
    except Exception as e:
        return f"Validation error: {str(e)}"

def write_file_content(file_path, content, file_type):
    """Write content to file with proper encoding"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return None
    except Exception as e:
        return str(e)
