// Sandra Benes Data Manager - JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize CodeMirror if on edit page
    if (document.getElementById('editor')) {
        initializeEditor();
    }
    
    // Initialize file upload functionality
    initializeFileUpload();
    
    // Initialize auto-save functionality
    initializeAutoSave();
    
    // Initialize form validation
    initializeValidation();
    
    // Update counters if editor exists
    if (document.getElementById('editor')) {
        updateCounters();
    }
});

let editor = null;
let autoSaveInterval = null;
let lastSavedContent = '';

function initializeEditor() {
    const textarea = document.getElementById('editor');
    if (!textarea) return;
    
    // Determine CodeMirror mode based on file type
    let mode = 'text/plain';
    if (fileType === 'json') {
        mode = 'application/json';
    } else if (fileType === 'csv') {
        mode = 'text/csv';
    }
    
    // Initialize CodeMirror
    editor = CodeMirror.fromTextArea(textarea, {
        mode: mode,
        theme: 'dracula',
        lineNumbers: true,
        lineWrapping: true,
        indentUnit: 2,
        tabSize: 2,
        matchBrackets: true,
        autoCloseBrackets: true,
        foldGutter: true,
        gutters: ["CodeMirror-linenumbers", "CodeMirror-foldgutter"],
        extraKeys: {
            "Ctrl-S": function(cm) {
                saveContent();
            },
            "Cmd-S": function(cm) {
                saveContent();
            }
        }
    });
    
    // Store initial content for reset functionality
    lastSavedContent = editor.getValue();
    
    // Update counters on change
    editor.on('change', function() {
        updateCounters();
        updateStatus('Modified');
    });
    
    // Initial counter update
    updateCounters();
}

function initializeFileUpload() {
    const uploadModal = document.getElementById('uploadModal');
    const fileInput = document.getElementById('file');
    
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                validateUploadFile(file);
            }
        });
    }
}

function initializeAutoSave() {
    const autoSaveCheckbox = document.getElementById('autoSave');
    if (!autoSaveCheckbox || !editor) return;
    
    autoSaveCheckbox.addEventListener('change', function() {
        if (this.checked) {
            startAutoSave();
        } else {
            stopAutoSave();
        }
    });
}

function initializeValidation() {
    const editForm = document.getElementById('editForm');
    if (!editForm) return;
    
    editForm.addEventListener('submit', function(e) {
        if (!validateContent()) {
            e.preventDefault();
            return false;
        }
        
        // Show confirmation for significant changes
        const currentContent = editor ? editor.getValue() : document.getElementById('editor').value;
        if (currentContent !== originalContent) {
            e.preventDefault();
            showSaveConfirmation();
        }
    });
}

function updateCounters() {
    const content = editor ? editor.getValue() : document.getElementById('editor').value;
    const lines = content.split('\n').length;
    const chars = content.length;
    
    const lineCountElement = document.getElementById('lineCount');
    const charCountElement = document.getElementById('charCount');
    
    if (lineCountElement) lineCountElement.textContent = `Lines: ${lines}`;
    if (charCountElement) charCountElement.textContent = `Characters: ${chars}`;
}

function updateStatus(message, type = 'info') {
    const statusElement = document.getElementById('statusText');
    if (!statusElement) return;
    
    statusElement.textContent = message;
    statusElement.className = `text-${type === 'error' ? 'danger' : type === 'success' ? 'success' : 'muted'}`;
    
    // Auto-clear status after 3 seconds
    setTimeout(() => {
        statusElement.textContent = 'Ready to edit';
        statusElement.className = 'text-muted';
    }, 3000);
}

function validateContent() {
    if (!editor) return true;
    
    const content = editor.getValue();
    
    try {
        if (fileType === 'json') {
            JSON.parse(content);
            updateStatus('Valid JSON', 'success');
            return true;
        } else if (fileType === 'csv') {
            // Basic CSV validation - check for consistent column counts
            const lines = content.trim().split('\n');
            if (lines.length > 1) {
                const headerCols = lines[0].split(',').length;
                for (let i = 1; i < lines.length; i++) {
                    const cols = lines[i].split(',').length;
                    if (cols !== headerCols) {
                        updateStatus(`Row ${i + 1} has ${cols} columns, expected ${headerCols}`, 'error');
                        return false;
                    }
                }
            }
            updateStatus('Valid CSV', 'success');
            return true;
        }
        
        updateStatus('Content validated', 'success');
        return true;
    } catch (error) {
        updateStatus(`Validation error: ${error.message}`, 'error');
        return false;
    }
}

function formatContent() {
    if (!editor) return;
    
    const content = editor.getValue();
    
    try {
        if (fileType === 'json') {
            const parsed = JSON.parse(content);
            const formatted = JSON.stringify(parsed, null, 2);
            editor.setValue(formatted);
            updateStatus('JSON formatted', 'success');
        } else if (fileType === 'csv') {
            // Basic CSV formatting - normalize spacing
            const lines = content.split('\n');
            const formatted = lines.map(line => 
                line.split(',').map(cell => cell.trim()).join(',')
            ).join('\n');
            editor.setValue(formatted);
            updateStatus('CSV formatted', 'success');
        } else {
            updateStatus('No formatting available for this file type', 'info');
        }
    } catch (error) {
        updateStatus(`Formatting error: ${error.message}`, 'error');
    }
}

function resetContent() {
    if (!editor) return;
    
    if (confirm('Are you sure you want to reset all changes? This cannot be undone.')) {
        editor.setValue(originalContent);
        updateStatus('Content reset', 'info');
        updateCounters();
    }
}

function startAutoSave() {
    if (autoSaveInterval) return;
    
    autoSaveInterval = setInterval(() => {
        const currentContent = editor ? editor.getValue() : '';
        if (currentContent !== lastSavedContent && validateContent()) {
            autoSave();
        }
    }, 30000); // 30 seconds
    
    showAutoSaveIndicator('Auto-save enabled', 'success');
}

function stopAutoSave() {
    if (autoSaveInterval) {
        clearInterval(autoSaveInterval);
        autoSaveInterval = null;
    }
    
    showAutoSaveIndicator('Auto-save disabled', 'info');
}

function autoSave() {
    const currentContent = editor ? editor.getValue() : '';
    const formData = new FormData();
    formData.append('content', currentContent);
    
    fetch(window.location.href.replace('/edit/', '/save/'), {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            lastSavedContent = currentContent;
            showAutoSaveIndicator('Auto-saved', 'success');
        } else {
            showAutoSaveIndicator('Auto-save failed', 'error');
        }
    })
    .catch(error => {
        showAutoSaveIndicator('Auto-save error', 'error');
        console.error('Auto-save error:', error);
    });
}

function showAutoSaveIndicator(message, type) {
    let indicator = document.getElementById('autoSaveIndicator');
    
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'autoSaveIndicator';
        indicator.className = 'auto-save-indicator alert';
        document.body.appendChild(indicator);
    }
    
    indicator.className = `auto-save-indicator alert alert-${type}`;
    indicator.textContent = message;
    indicator.classList.add('show');
    
    setTimeout(() => {
        indicator.classList.remove('show');
    }, 2000);
}

function saveContent() {
    document.getElementById('editForm').submit();
}

function showSaveConfirmation() {
    const modal = new bootstrap.Modal(document.getElementById('saveConfirmModal'));
    modal.show();
}

function validateUploadFile(file) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = ['.csv', '.json', '.txt', '.md', '.log'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    
    if (file.size > maxSize) {
        alert('File is too large. Maximum size is 16MB.');
        return false;
    }
    
    if (!allowedTypes.includes(fileExt)) {
        alert('Unsupported file type. Please upload CSV, JSON, TXT, MD, or LOG files.');
        return false;
    }
    
    return true;
}

function confirmDelete(filename) {
    document.getElementById('deleteFileName').textContent = filename;
    document.getElementById('deleteForm').action = `/delete/${filename}`;
    
    const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
    modal.show();
}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+S or Cmd+S to save
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        if (document.getElementById('editForm')) {
            saveContent();
        }
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
        const modals = document.querySelectorAll('.modal.show');
        modals.forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        });
    }
});

// Prevent accidental page close with unsaved changes
window.addEventListener('beforeunload', function(e) {
    if (editor) {
        const currentContent = editor.getValue();
        if (currentContent !== originalContent) {
            e.preventDefault();
            e.returnValue = 'You have unsaved changes. Are you sure you want to leave?';
            return e.returnValue;
        }
    }
});
