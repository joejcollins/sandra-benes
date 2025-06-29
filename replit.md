# Sandra Benes Data Manager

## Overview

The Sandra Benes Data Manager is a Flask-based web application for managing and editing scientific data files. Named after the Data Section Coordinator from Space: 1999, this system provides a comprehensive interface for viewing, editing, uploading, and organizing various file formats including CSV, JSON, and text files.

## System Architecture

### Frontend Architecture
- **Template Engine**: Jinja2 templates with Bootstrap for responsive UI
- **CSS Framework**: Bootstrap with dark theme customization
- **JavaScript**: Vanilla JavaScript with CodeMirror for syntax highlighting
- **Icons**: Feather Icons for consistent iconography

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Architecture Pattern**: Modular Flask application with separated concerns
- **File Structure**: 
  - `app.py`: Main application configuration and initialization
  - `routes.py`: HTTP route handlers and business logic
  - `utils.py`: Utility functions for file operations
  - `main.py`: Application entry point

### Data Storage
- **Primary Storage**: File system-based storage in `/data` directory
- **File Types Supported**: CSV, JSON, TXT, MD, LOG files
- **Configuration**: JSON-based configuration file (`config.json`)
- **No Database**: Direct file system operations for simplicity

## Key Components

### File Management System
- **Upload Mechanism**: Secure file upload with validation and size limits (16MB)
- **File Operations**: View, edit, download, and delete operations
- **Security**: Filename sanitization using `secure_filename()`
- **File Type Detection**: Extension-based file type identification

### Editor Component
- **Syntax Highlighting**: CodeMirror integration for multiple file formats
- **Auto-save**: Configurable auto-save functionality (30-second intervals)
- **Validation**: Real-time content validation for structured formats
- **Theme**: Dark theme (Dracula) for better user experience

### Search and Filtering
- **Text Search**: Case-insensitive filename search
- **Type Filtering**: Filter by file type (CSV, JSON, text)
- **Sorting**: Alphabetical sorting by filename
- **Metadata Display**: File size, modification date, and type information

## Data Flow

1. **File Upload**: Files are uploaded via web form → validated → stored in `/data` directory
2. **File Listing**: Directory scan → metadata extraction → template rendering
3. **File Viewing**: File read → content parsing → format-specific display
4. **File Editing**: Content load → CodeMirror editor → validation → save operation
5. **Search/Filter**: Query processing → file list filtering → UI update

## External Dependencies

### Frontend Dependencies
- **Bootstrap**: UI framework and components
- **CodeMirror**: Code editor with syntax highlighting
- **Feather Icons**: Icon library for UI elements

### Backend Dependencies
- **Flask**: Core web framework
- **Werkzeug**: WSGI utilities and security helpers
- **Python Standard Library**: File operations, JSON/CSV handling

### CDN Resources
- Bootstrap CSS/JS from Replit CDN
- CodeMirror from CDNJS
- Feather Icons from unpkg

## Deployment Strategy

### Development Environment
- **Host**: `0.0.0.0` for external access
- **Port**: 5000 (configurable)
- **Debug Mode**: Enabled for development
- **Logging**: Debug-level logging configured

### Production Considerations
- **Proxy Support**: ProxyFix middleware for reverse proxy deployment
- **Security**: Session secret from environment variables
- **File Limits**: 16MB upload limit configured
- **Error Handling**: Comprehensive error handling with user feedback

### Environment Variables
- `SESSION_SECRET`: Flask session encryption key
- Development defaults provided for immediate functionality

## Changelog
- June 29, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.