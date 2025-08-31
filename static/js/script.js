// Global variables
let currentResult = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    initializeEventListeners();
});

function initializeForm() {
    // Set default values
    document.getElementById('duration').value = 'short';
    document.getElementById('cta').value = 'सत्य सामने आए';
}

function initializeEventListeners() {
    // Form submission
    document.getElementById('scriptForm').addEventListener('submit', handleFormSubmit);
    
    // Copy all button
    document.getElementById('copyAllBtn').addEventListener('click', copyAllContent);
    
    // Real-time character count for title
    document.getElementById('resultTitle').addEventListener('input', updateTitleLength);
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    // Validate form
    if (!form.checkValidity()) {
        form.classList.add('was-validated');
        return;
    }
    
    // Show loading state
    showLoading();
    
    try {
        // Prepare data
        const data = {
            topic: formData.get('topic'),
            location: formData.get('location'),
            victim_role: formData.get('victim_role'),
            aspiration: formData.get('aspiration') || 'civil services',
            duration: formData.get('duration'),
            timeline: formData.get('timeline') ? formData.get('timeline').split('\n').filter(line => line.trim()) : [],
            official_version: formData.get('official_version'),
            family_version: formData.get('family_version'),
            must_include: formData.get('must_include') ? formData.get('must_include').split('\n').filter(line => line.trim()) : [],
            keywords: formData.get('keywords') ? formData.get('keywords').split(',').map(k => k.trim()).filter(k => k) : [],
            cta: formData.get('cta') || 'सत्य सामने आए'
        };
        
        // Make API call
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            displayResult(result);
        } else {
            showError(result.error || 'Unknown error occurred');
        }
        
    } catch (error) {
        console.error('Error:', error);
        showError('Network error. Please check your connection and try again.');
    }
}

function showLoading() {
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('loadingSpinner').style.display = 'block';
    document.getElementById('copyAllBtn').style.display = 'none';
}

function showError(message) {
    document.getElementById('loadingSpinner').style.display = 'none';
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('copyAllBtn').style.display = 'none';
    
    document.getElementById('errorText').textContent = message;
    document.getElementById('errorMessage').style.display = 'block';
}

function displayResult(result) {
    currentResult = result;
    
    document.getElementById('loadingSpinner').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    
    // Populate result fields
    document.getElementById('resultTitle').value = result.title || '';
    document.getElementById('resultScript').value = result.vo_script || '';
    document.getElementById('resultOnScreen').value = Array.isArray(result.on_screen_text) 
        ? result.on_screen_text.join('\n') : result.on_screen_text || '';
    document.getElementById('resultDescription').value = result.description || '';
    document.getElementById('resultHashtags').value = Array.isArray(result.hashtags) 
        ? result.hashtags.join(' ') : result.hashtags || '';
    
    // Update notes
    if (result.notes) {
        const notesHtml = `
            <div><strong>Pace:</strong> ${result.notes.pace_wpm || 150} WPM</div>
            <div><strong>TTS Tags:</strong> ${result.notes.tts_tags_used ? 'Used' : 'Not used'}</div>
            <div><strong>Legal Framing:</strong> ${result.notes.legal_framing || 'Neutral'}</div>
        `;
        document.getElementById('resultNotes').innerHTML = notesHtml;
    }
    
    // Update title length
    updateTitleLength();
    
    // Show result container and copy button
    document.getElementById('resultContainer').style.display = 'block';
    document.getElementById('copyAllBtn').style.display = 'inline-block';
}

function updateTitleLength() {
    const title = document.getElementById('resultTitle').value;
    const length = title.length;
    const lengthElement = document.getElementById('titleLength');
    
    if (lengthElement) {
        lengthElement.textContent = length;
        lengthElement.className = length > 65 ? 'text-warning' : 'text-muted';
    }
}

function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    
    if (element) {
        element.select();
        element.setSelectionRange(0, 99999); // For mobile devices
        
        try {
            document.execCommand('copy');
            showCopyToast();
        } catch (err) {
            // Fallback for modern browsers
            navigator.clipboard.writeText(element.value).then(() => {
                showCopyToast();
            }).catch(() => {
                alert('Failed to copy content');
            });
        }
    }
}

function copyAllContent() {
    if (!currentResult) return;
    
    const allContent = `
TITLE:
${currentResult.title || ''}

VOICE OVER SCRIPT:
${currentResult.vo_script || ''}

ON-SCREEN TEXT:
${Array.isArray(currentResult.on_screen_text) ? currentResult.on_screen_text.join('\n') : currentResult.on_screen_text || ''}

DESCRIPTION:
${currentResult.description || ''}

HASHTAGS:
${Array.isArray(currentResult.hashtags) ? currentResult.hashtags.join(' ') : currentResult.hashtags || ''}
    `.trim();
    
    try {
        navigator.clipboard.writeText(allContent).then(() => {
            showCopyToast();
        }).catch(() => {
            // Fallback
            const textArea = document.createElement('textarea');
            textArea.value = allContent;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            showCopyToast();
        });
    } catch (err) {
        alert('Failed to copy content');
    }
}

function showCopyToast() {
    const toast = new bootstrap.Toast(document.getElementById('copyToast'));
    toast.show();
}

// Form validation
(function() {
    'use strict';
    
    // Fetch all the forms we want to apply custom Bootstrap validation styles to
    const forms = document.querySelectorAll('.needs-validation');
    
    // Loop over them and prevent submission
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
})();
