// Global variables
let currentResult = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeForm();
    initializeEventListeners();
});

function initializeForm() {
    // Set default values for both duration selectors
    const humanizeDuration = document.getElementById('humanize_duration');
    const generateDuration = document.getElementById('generate_duration');
    
    if (humanizeDuration) humanizeDuration.value = '45';
    if (generateDuration) generateDuration.value = '45';
    
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
    
    // API key management
    initializeApiKeyManagement();
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
        
        // Include API key if available
        const apiKey = getStoredApiKey();
        if (apiKey) {
            data.api_key = apiKey;
        }
        
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
        
        // Provide specific solutions based on error type
        let errorMessage = 'API connection failed. ';
        if (!getStoredApiKey()) {
            errorMessage += 'Please set your Gemini API key in the API Settings menu (top right). Get your free key from Google AI Studio.';
        } else if (error.message.includes('fetch')) {
            errorMessage += 'Check your internet connection and try again. If the problem persists, verify your API key is valid.';
        } else if (error.message.includes('json')) {
            errorMessage += 'Server error occurred. The service may be temporarily unavailable. Try again in a few moments.';
        } else {
            errorMessage += 'Unexpected error. Please refresh the page and try again.';
        }
        
        showError(errorMessage);
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
        const notesContainer = document.getElementById('resultNotes');
        notesContainer.innerHTML = ''; // Clear existing content
        
        // Create safe DOM elements
        const paceDiv = document.createElement('div');
        const paceStrong = document.createElement('strong');
        paceStrong.textContent = 'Pace:';
        paceDiv.appendChild(paceStrong);
        paceDiv.appendChild(document.createTextNode(' ' + (result.notes.pace_wpm || 150) + ' WPM'));
        
        const ttsDiv = document.createElement('div');
        const ttsStrong = document.createElement('strong');
        ttsStrong.textContent = 'TTS Tags:';
        ttsDiv.appendChild(ttsStrong);
        ttsDiv.appendChild(document.createTextNode(' ' + (result.notes.tts_tags_used ? 'Used' : 'Not used')));
        
        const legalDiv = document.createElement('div');
        const legalStrong = document.createElement('strong');
        legalStrong.textContent = 'Legal Framing:';
        legalDiv.appendChild(legalStrong);
        legalDiv.appendChild(document.createTextNode(' ' + (result.notes.legal_framing || 'Neutral')));
        
        notesContainer.appendChild(paceDiv);
        notesContainer.appendChild(ttsDiv);
        notesContainer.appendChild(legalDiv);
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
    
    if (!mode1 || !mode2) return; // Safety check
    
    const isHumanizeMode = mode1.checked;
    
    const buttonText = document.getElementById('buttonText');
    const humanizeSection = document.getElementById('humanizeSection');
    const generateSection = document.getElementById('generateSection');
    const rawScriptInput = document.getElementById('raw_script');
    const topicInput = document.getElementById('topic');
    const genreInput = document.getElementById('genre');
    const mode1Card = document.getElementById('mode1Card');
    const mode2Card = document.getElementById('mode2Card');
    
    // Update card styling
    if (mode1Card) mode1Card.classList.toggle('active', isHumanizeMode);
    if (mode2Card) mode2Card.classList.toggle('active', !isHumanizeMode);
    
    if (isHumanizeMode) {
        // Mode 1: Humanize
        if (buttonText) buttonText.textContent = 'Humanize Script';
        if (humanizeSection) humanizeSection.style.display = 'block';
        if (generateSection) generateSection.style.display = 'none';
        if (rawScriptInput) rawScriptInput.required = true;
        
        // Remove required from generate mode fields
        if (topicInput) topicInput.required = false;
        if (genreInput) genreInput.required = false;
    } else {
        // Mode 2: Generate
        if (buttonText) buttonText.textContent = 'Generate Script';
        if (humanizeSection) humanizeSection.style.display = 'none';
        if (generateSection) generateSection.style.display = 'block';
        if (rawScriptInput) rawScriptInput.required = false;
        
        // Add required to generate mode fields
        if (topicInput) topicInput.required = true;
        if (genreInput) genreInput.required = true;
        
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

// API Key Management Functions
function initializeApiKeyManagement() {
    // Initialize API key status
    updateApiKeyStatus();
    
    // API key input toggle
    document.getElementById('toggleApiKey').addEventListener('click', function() {
        const input = document.getElementById('apiKeyInput');
        const icon = this.querySelector('i');
        
        if (input.type === 'password') {
            input.type = 'text';
            icon.className = 'fas fa-eye-slash';
        } else {
            input.type = 'password';
            icon.className = 'fas fa-eye';
        }
    });
    
    // Save API key
    document.getElementById('saveApiKey').addEventListener('click', function() {
        const apiKey = document.getElementById('apiKeyInput').value.trim();
        
        if (!apiKey) {
            showToast('Please enter an API key', 'warning');
            return;
        }
        
        // Validate API key format (basic validation)
        if (!apiKey.startsWith('AIza') || apiKey.length < 30) {
            showToast('Invalid API key format. Please check your Gemini API key.', 'warning');
            return;
        }
        
        // Store API key in localStorage
        localStorage.setItem('gemini_api_key', apiKey);
        updateApiKeyStatus();
        showToast('API key saved successfully!', 'success');
        
        // Clear the input
        document.getElementById('apiKeyInput').value = '';
    });
    
    // Clear API key
    document.getElementById('clearApiKey').addEventListener('click', function() {
        localStorage.removeItem('gemini_api_key');
        updateApiKeyStatus();
        document.getElementById('apiKeyInput').value = '';
        showToast('API key cleared', 'info');
    });
    
    // Load stored API key on page load
    const storedKey = getStoredApiKey();
    if (storedKey) {
        // Show partial key for security
        document.getElementById('apiKeyInput').placeholder = `Key saved: ${storedKey.substring(0, 8)}...`;
    }
}

function getStoredApiKey() {
    return localStorage.getItem('gemini_api_key');
}

function updateApiKeyStatus() {
    const statusElement = document.getElementById('apiKeyStatus');
    const apiKey = getStoredApiKey();
    
    if (apiKey) {
        statusElement.textContent = 'Configured';
        statusElement.className = 'text-success';
    } else {
        statusElement.textContent = 'Not configured';
        statusElement.className = 'text-warning';
    }
}

function showToast(message, type = 'info') {
    // Create toast if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    const toastId = 'toast_' + Date.now();
    const iconClass = type === 'success' ? 'fa-check' : type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle';
    const bgClass = type === 'success' ? 'bg-success' : type === 'warning' ? 'bg-warning' : 'bg-info';
    
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-body ${bgClass} text-white">
                <i class="fas ${iconClass} me-2"></i>
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}
