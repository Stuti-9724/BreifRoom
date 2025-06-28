// Briefroom JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    initializeFileUpload();
    initializeTextInput();
    initializeFormSubmission();
});

// File Upload Functionality
function initializeFileUpload() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('audioFile');
    const uploadPreview = document.getElementById('uploadPreview');
    const uploadPlaceholder = uploadArea.querySelector('.upload-placeholder');
    const audioSubmit = document.getElementById('audioSubmit');
    const removeFileBtn = document.getElementById('removeFile');

    if (!uploadArea || !fileInput) return;

    // Click to upload
    uploadArea.addEventListener('click', function(e) {
        if (e.target.id !== 'removeFile') {
            fileInput.click();
        }
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            const file = files[0];
            if (isValidAudioFile(file)) {
                fileInput.files = files;
                showFilePreview(file);
            } else {
                showError('Please upload only MP3 or WAV files.');
            }
        }
    });

    // File input change
    fileInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            if (isValidAudioFile(file)) {
                showFilePreview(file);
            } else {
                showError('Please upload only MP3 or WAV files.');
                fileInput.value = '';
            }
        }
    });

    // Remove file
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            clearFileSelection();
        });
    }

    function isValidAudioFile(file) {
        const validTypes = ['audio/mpeg', 'audio/mp3', 'audio/wav'];
        const validExtensions = ['.mp3', '.wav'];
        const fileName = file.name.toLowerCase();
        
        return validTypes.includes(file.type) || 
               validExtensions.some(ext => fileName.endsWith(ext));
    }

    function showFilePreview(file) {
        const fileName = document.getElementById('fileName');
        const fileSize = document.getElementById('fileSize');
        
        if (fileName && fileSize) {
            fileName.textContent = file.name;
            fileSize.textContent = formatFileSize(file.size);
            
            uploadPlaceholder.classList.add('d-none');
            uploadPreview.classList.remove('d-none');
            
            if (audioSubmit) {
                audioSubmit.disabled = false;
            }
            
            // Re-initialize feather icons for the new elements
            feather.replace();
        }
    }

    function clearFileSelection() {
        fileInput.value = '';
        uploadPlaceholder.classList.remove('d-none');
        uploadPreview.classList.add('d-none');
        
        if (audioSubmit) {
            audioSubmit.disabled = true;
        }
    }

    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
}

// Text Input Functionality
function initializeTextInput() {
    const textContent = document.getElementById('textContent');
    const charCount = document.getElementById('charCount');
    const textSubmit = document.getElementById('textSubmit');

    if (!textContent) return;

    textContent.addEventListener('input', function() {
        const length = textContent.value.length;
        
        if (charCount) {
            charCount.textContent = length.toLocaleString();
        }
        
        if (textSubmit) {
            textSubmit.disabled = length === 0;
        }
    });
}

// Form Submission with Processing Modal
function initializeFormSubmission() {
    const audioForm = document.getElementById('audioForm');
    const textForm = document.getElementById('textForm');
    
    if (audioForm) {
        audioForm.addEventListener('submit', function(e) {
            showProcessingModal('audio');
        });
    }
    
    if (textForm) {
        textForm.addEventListener('submit', function(e) {
            showProcessingModal('text');
        });
    }
}

function showProcessingModal(contentType) {
    const modal = new bootstrap.Modal(document.getElementById('processingModal'));
    const statusElement = document.getElementById('processingStatus');
    
    if (statusElement) {
        if (contentType === 'audio') {
            statusElement.textContent = 'Transcribing audio file...';
            
            setTimeout(() => {
                statusElement.textContent = 'Analyzing content and generating brief...';
            }, 3000);
        } else {
            statusElement.textContent = 'Analyzing content and generating brief...';
        }
    }
    
    modal.show();
}

// Copy to Clipboard Functionality
function copyToClipboard(sessionId) {
    fetch(`/api/copy-content/${sessionId}`)
        .then(response => response.json())
        .then(data => {
            if (data.content) {
                navigator.clipboard.writeText(data.content).then(function() {
                    showCopyToast();
                }).catch(function(err) {
                    console.error('Could not copy text: ', err);
                    showError('Failed to copy to clipboard');
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Failed to copy content');
        });
}

function showCopyToast() {
    const toastElement = document.getElementById('copyToast');
    if (toastElement) {
        const toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Re-initialize feather icons in the toast
        feather.replace();
    }
}

// Error Handling
function showError(message) {
    // Create a temporary alert
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the main container
    const container = document.querySelector('main.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            const alert = bootstrap.Alert.getOrCreateInstance(alertDiv);
            alert.close();
        }, 5000);
    }
}

// Tab switching functionality
document.addEventListener('shown.bs.tab', function(event) {
    // Re-initialize feather icons when tabs are switched
    feather.replace();
});

// Initialize feather icons on dynamic content
function initializeFeatherIcons() {
    feather.replace();
}

// Call this whenever new content is added to the DOM
document.addEventListener('DOMContentLoaded', initializeFeatherIcons);
