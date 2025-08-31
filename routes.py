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
            # Validate required fields for humanize mode
            if not form_data.get('raw_script'):
                return jsonify({
                    'error': 'Raw script is required for humanization mode'
                }), 400
        else:
            # Validate required fields for generate mode
            required_fields = ['topic', 'location', 'victim_role', 'duration']
            missing_fields = [field for field in required_fields if not form_data.get(field)]
            
            if missing_fields:
                return jsonify({
                    'error': f'Missing required fields: {", ".join(missing_fields)}'
                }), 400
        
        if mode == 'humanize':
            # Handle humanization mode
            result = humanize_hindi_script(form_data.get('raw_script'))
        else:
            # Handle generation mode
            # Parse timeline if provided as JSON string
            timeline = form_data.get('timeline', '[]')
            if isinstance(timeline, str):
                try:
                    timeline = json.loads(timeline)
                except json.JSONDecodeError:
                    timeline = timeline.split('\n') if timeline else []
            
            # Parse must_include items
            must_include = form_data.get('must_include', '[]')
            if isinstance(must_include, str):
                try:
                    must_include = json.loads(must_include)
                except json.JSONDecodeError:
                    must_include = must_include.split('\n') if must_include else []
            
            # Parse keywords
            keywords = form_data.get('keywords', '[]')
            if isinstance(keywords, str):
                try:
                    keywords = json.loads(keywords)
                except json.JSONDecodeError:
                    keywords = keywords.split(',') if keywords else []
            
            # Build input payload for Gemini API with YouTube optimization
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
                "case": {
                    "topic": form_data.get('topic'),
                    "location": form_data.get('location'),
                    "victim_role": form_data.get('victim_role'),
                    "aspiration": form_data.get('aspiration', 'civil services'),
                    "timeline": timeline,
                    "official_version": form_data.get('official_version', ''),
                    "family_version": form_data.get('family_version', ''),
                    "must_include": must_include,
                    "cta": form_data.get('cta', 'सत्य सामने आए')
                },
                "seo": {
                    "primary_keywords": keywords,
                    "hashtag_style": "youtube_optimized",
                    "audience": "16-35, Hindi, news/moral storytelling",
                    "platform": "youtube",
                    "optimization_goal": "viral_reach"
                }
            }
            
            # Generate script using Gemini API
            result = generate_hindi_script(input_payload)
        
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
