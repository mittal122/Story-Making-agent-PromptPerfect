import json
import logging
from flask import render_template, request, jsonify, flash
from app import app
from gemini_service import generate_hindi_script, humanize_hindi_script

@app.route('/')
def index():
    """Main page with the script generation form"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
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
                result = humanize_hindi_script(form_data.get('raw_script'), duration_seconds)
            except Exception as api_error:
                logging.error(f"Gemini API error in humanize mode: {str(api_error)}")
                return jsonify({
                    'error': 'Script humanization service is temporarily unavailable. Please try again in a few moments.'
                }), 503
        else:
            # Mode 2: Handle generation mode
            # No additional parsing needed
            
            # Build input payload for genre-based generation
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
                result = generate_hindi_script(input_payload)
            except Exception as api_error:
                logging.error(f"Gemini API error in generate mode: {str(api_error)}")
                return jsonify({
                    'error': 'Script generation service is temporarily unavailable. Please try again in a few moments.'
                }), 503
        
        if result.get('error'):
            return jsonify({'error': result['error']}), 500
        
        return jsonify(result)
        
    except Exception as e:
        logging.error(f"Error processing script: {str(e)}")
        return jsonify({'error': f'Script processing failed: {str(e)}'}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html'), 500
