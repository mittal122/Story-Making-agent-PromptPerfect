// Global variables
let currentResult = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    initializeEventListeners();
});

function initializeForm() {
    // Set default values
    document.getElementById('duration_seconds').value = '45';
    
    // Initialize mode
    handleModeChange();
}

function initializeEventListeners() {
    // Form submission
    document.getElementById('scriptForm').addEventListener('submit', handleFormSubmit);
    
    // Copy all button
    document.getElementById('copyAllBtn').addEventListener('click', copyAllContent);
    
    // Real-time character count for title
    document.getElementById('resultTitle').addEventListener('input', updateTitleLength);
    
    // Mode selection
    document.getElementById('mode1').addEventListener('change', handleModeChange);
    document.getElementById('mode2').addEventListener('change', handleModeChange);
    
    // Genre selection
    document.getElementById('genre').addEventListener('change', handleGenreChange);
    
    // Mode card clicks
    document.getElementById('mode1Card').addEventListener('click', () => {
        document.getElementById('mode1').checked = true;
        handleModeChange();
    });
    document.getElementById('mode2Card').addEventListener('click', () => {
        document.getElementById('mode2').checked = true;
        handleModeChange();
    });
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
        const isHumanizeMode = document.getElementById('mode1').checked;
        
        // Prepare data based on mode
        const data = {
            mode: isHumanizeMode ? 'humanize' : 'generate'
        };
        
        if (isHumanizeMode) {
            // Mode 1: Humanize - send raw script and duration
            data.raw_script = formData.get('raw_script');
            data.duration_seconds = parseInt(formData.get('humanize_duration')) || 45;
        } else {
            // Mode 2: Generate - send topic, genre, description, and duration
            data.topic = formData.get('topic');
            data.genre = formData.get('genre');
            data.description = formData.get('description') || '';
            data.duration_seconds = parseInt(formData.get('generate_duration')) || 45;
            data.keywords = formData.get('keywords') ? formData.get('keywords').split(',').map(k => k.trim()).filter(k => k) : [];
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
    
    // Show button spinner
    const generateBtn = document.getElementById('generateBtn');
    const buttonSpinner = document.getElementById('buttonSpinner');
    const buttonText = document.getElementById('buttonText');
    
    generateBtn.disabled = true;
    buttonSpinner.style.display = 'inline-block';
    buttonText.textContent = 'Generating...';
}

function showError(message) {
    document.getElementById('loadingSpinner').style.display = 'none';
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('emptyState').style.display = 'none';
    document.getElementById('copyAllBtn').style.display = 'none';
    
    document.getElementById('errorText').textContent = message;
    document.getElementById('errorMessage').style.display = 'block';
    
    // Reset button state
    resetButtonState();
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
    
    // Display YouTube tags if available
    if (result.youtube_tags && result.youtube_tags.length > 0) {
        document.getElementById('resultYoutubeTags').value = Array.isArray(result.youtube_tags) 
            ? result.youtube_tags.join(', ') : result.youtube_tags || '';
        document.getElementById('youtubeTagsSection').style.display = 'block';
    } else {
        document.getElementById('youtubeTagsSection').style.display = 'none';
    }
    
    // Update title length
    updateTitleLength();
    
    // Show result container and copy button
    document.getElementById('resultContainer').style.display = 'block';
    document.getElementById('copyAllBtn').style.display = 'inline-block';
    
    // Reset button state
    resetButtonState();
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

YOUTUBE TAGS:
${Array.isArray(currentResult.youtube_tags) ? currentResult.youtube_tags.join(', ') : currentResult.youtube_tags || ''}
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

function handleModeChange() {
    const mode1 = document.getElementById('mode1');
    const mode2 = document.getElementById('mode2');
    const isHumanizeMode = mode1.checked;
    
    const buttonText = document.getElementById('buttonText');
    const humanizeSection = document.getElementById('humanizeSection');
    const generateSection = document.getElementById('generateSection');
    const rawScriptInput = document.getElementById('raw_script');
    const topicInput = document.getElementById('topic');
    const genreInput = document.getElementById('genre');
    
    // Update card styling
    document.getElementById('mode1Card').classList.toggle('active', isHumanizeMode);
    document.getElementById('mode2Card').classList.toggle('active', !isHumanizeMode);
    
    if (isHumanizeMode) {
        // Mode 1: Humanize
        buttonText.textContent = 'Humanize Script';
        humanizeSection.style.display = 'block';
        generateSection.style.display = 'none';
        rawScriptInput.required = true;
        
        // Remove required from generate mode fields
        topicInput.required = false;
        genreInput.required = false;
    } else {
        // Mode 2: Generate
        buttonText.textContent = 'Generate Script';
        humanizeSection.style.display = 'none';
        generateSection.style.display = 'block';
        rawScriptInput.required = false;
        
        // Add required to generate mode fields
        topicInput.required = true;
        genreInput.required = true;
        
        // Trigger genre change to show/hide options
        handleGenreChange();
    }
}

function handleGenreChange() {
    // Genre change handler - no additional options needed now
    const genre = document.getElementById('genre').value;
    // All genres use the same form fields now
}

function resetButtonState() {
    const generateBtn = document.getElementById('generateBtn');
    const buttonSpinner = document.getElementById('buttonSpinner');
    const buttonText = document.getElementById('buttonText');
    const isHumanizeMode = document.getElementById('mode1').checked;
    
    generateBtn.disabled = false;
    buttonSpinner.style.display = 'none';
    buttonText.textContent = isHumanizeMode ? 'Humanize Script' : 'Generate Script';
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
