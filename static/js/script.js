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
    
    // Initialize mode toggle
    handleModeToggle();
}

function initializeEventListeners() {
    // Form submission
    document.getElementById('scriptForm').addEventListener('submit', handleFormSubmit);
    
    // Copy all button
    document.getElementById('copyAllBtn').addEventListener('click', copyAllContent);
    
    // Real-time character count for title
    document.getElementById('resultTitle').addEventListener('input', updateTitleLength);
    
    // Mode toggle
    document.getElementById('modeToggle').addEventListener('change', handleModeToggle);
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
        // Check mode
        const isHumanizeMode = document.getElementById('modeToggle').checked;
        
        // Prepare data based on mode
        const data = {
            mode: isHumanizeMode ? 'humanize' : 'generate'
        };
        
        if (isHumanizeMode) {
            // Humanize mode - only send raw script
            data.raw_script = formData.get('raw_script');
        } else {
            // Generate mode - send all form fields
            data.topic = formData.get('topic');
            data.location = formData.get('location');
            data.victim_role = formData.get('victim_role');
            data.aspiration = formData.get('aspiration') || 'civil services';
            data.duration = formData.get('duration');
            data.timeline = formData.get('timeline') ? formData.get('timeline').split('\n').filter(line => line.trim()) : [];
            data.official_version = formData.get('official_version');
            data.family_version = formData.get('family_version');
            data.must_include = formData.get('must_include') ? formData.get('must_include').split('\n').filter(line => line.trim()) : [];
            data.keywords = formData.get('keywords') ? formData.get('keywords').split(',').map(k => k.trim()).filter(k => k) : [];
            data.cta = formData.get('cta') || 'सत्य सामने आए';
        }
        
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

function handleModeToggle() {
    const modeToggle = document.getElementById('modeToggle');
    const isHumanizeMode = modeToggle.checked;
    
    const modeLabel = document.getElementById('modeLabel');
    const modeDescription = document.getElementById('modeDescription');
    const buttonText = document.getElementById('buttonText');
    const rawScriptSection = document.getElementById('rawScriptSection');
    const generateModeFields = document.getElementById('generateModeFields');
    const rawScriptInput = document.getElementById('raw_script');
    
    if (isHumanizeMode) {
        // Switch to humanize mode
        modeLabel.textContent = 'Humanize Existing Script';
        modeDescription.textContent = 'Make an existing script sound more natural and human-like';
        buttonText.textContent = 'Humanize Script';
        rawScriptSection.style.display = 'block';
        generateModeFields.style.display = 'none';
        rawScriptInput.required = true;
        
        // Remove required from generate mode fields
        document.getElementById('topic').required = false;
        document.getElementById('location').required = false;
        document.getElementById('victim_role').required = false;
        document.getElementById('duration').required = false;
    } else {
        // Switch to generate mode
        modeLabel.textContent = 'Generate New Script';
        modeDescription.textContent = 'Create a new Hindi script from case details and timeline';
        buttonText.textContent = 'Generate Script';
        rawScriptSection.style.display = 'none';
        generateModeFields.style.display = 'block';
        rawScriptInput.required = false;
        
        // Add required to generate mode fields
        document.getElementById('topic').required = true;
        document.getElementById('location').required = true;
        document.getElementById('victim_role').required = true;
        document.getElementById('duration').required = true;
    }
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
