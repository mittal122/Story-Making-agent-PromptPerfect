import os
import logging
from flask import Flask, request, jsonify
from gemini_service import generate_hindi_script, humanize_hindi_script

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")

@app.route('/api/generate', methods=['POST'])
def generate_script():
    """Handle script generation requests"""
    try:
        # Get form data
        form_data = request.get_json() if request.is_json else request.form.to_dict()
        
        # Check mode
        mode = form_data.get('mode', 'generate')
        
        if mode == 'humanize':
            # Mode 1: Humanize - Validate required fields
            if not form_data.get('raw_script'):
                return jsonify({
                    'error': 'Raw script is required for humanization mode'
                }), 400
        else:
            # Mode 2: Generate - Validate required fields
            required_fields = ['topic', 'genre']
            missing_fields = [field for field in required_fields if not form_data.get(field)]
            
            if missing_fields:
                return jsonify({
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400
        
        logging.info(f"Processing {mode} request")
        
        if mode == 'humanize':
            # Mode 1: Handle humanization mode
            duration_seconds = int(form_data.get('duration_seconds', 45))
            try:
                custom_api_key = form_data.get('api_key')
                result = humanize_hindi_script(form_data.get('raw_script'), duration_seconds, custom_api_key)
            except Exception as api_error:
                logging.error(f"Gemini API error in humanize mode: {str(api_error)}")
                
                # Provide specific error guidance
                if '401' in str(api_error) or 'UNAUTHENTICATED' in str(api_error):
                    error_msg = 'Invalid API key. Please check your Gemini API key in the API Settings menu (top right). Get your free key from Google AI Studio.'
                elif '503' in str(api_error) or 'overloaded' in str(api_error):
                    error_msg = 'Gemini service is overloaded. Please wait a few minutes and try again, or use your own API key for priority access.'
                elif '429' in str(api_error) or 'quota' in str(api_error):
                    error_msg = 'API quota exceeded. Please use your own Gemini API key for unlimited access, or try again later.'
                else:
                    error_msg = 'Script humanization service is temporarily unavailable. Please check your internet connection and try again.'
                
                return jsonify({'error': error_msg}), 503
        else:
            # Mode 2: Handle generation mode
            duration_seconds = int(form_data.get('duration_seconds', 45))
            input_payload = {
                "api_key_mode": "env",
                "generation": {
                    "duration_seconds": duration_seconds,
                    "duration_type": "short" if duration_seconds <= 60 else "long",
                    "language": "hi",
                    "voice_tags": True,
                    "youtube_optimized": True,
                    "algorithm_focus": "maximum_reach"
                },
                "content": {
                    "topic": form_data.get('topic'),
                    "genre": form_data.get('genre'),
                    "description": form_data.get('description', '')
                },
                "seo": {
                    "hashtag_style": "youtube_optimized",
                    "audience": "16-35, Hindi, storytelling",
                    "platform": "youtube",
                    "optimization_goal": "viral_reach"
                }
            }
            
            # Generate script using Gemini API
            try:
                custom_api_key = form_data.get('api_key')
                result = generate_hindi_script(input_payload, custom_api_key)
            except Exception as api_error:
                logging.error(f"Gemini API error in generate mode: {str(api_error)}")
                
                # Provide specific error guidance  
                if '401' in str(api_error) or 'UNAUTHENTICATED' in str(api_error):
                    error_msg = 'Invalid API key. Please check your Gemini API key in the API Settings menu (top right). Get your free key from Google AI Studio.'
                elif '503' in str(api_error) or 'overloaded' in str(api_error):
                    error_msg = 'Gemini service is overloaded. Please wait a few minutes and try again, or use your own API key for priority access.'
                elif '429' in str(api_error) or 'quota' in str(api_error):
                    error_msg = 'API quota exceeded. Please use your own Gemini API key for unlimited access, or try again later.'
                else:
                    error_msg = 'Script generation service is temporarily unavailable. Please check your internet connection and try again.'
                
                return jsonify({'error': error_msg}), 503
        
        if result.get('error'):
            return jsonify({'error': result['error']}), 500
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error processing script: {str(e)}")
        return jsonify({'error': f'Script processing failed: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'PromptPerfect API is running'})

# For Vercel serverless functions
app = app
