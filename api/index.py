import os
import logging
from flask import Flask, render_template, request, jsonify, flash
from werkzeug.middleware.proxy_fix import ProxyFix
from gemini_service import generate_hindi_script, humanize_hindi_script

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_script():
    try:
        form_data = request.get_json() if request.is_json else request.form.to_dict()
        mode = form_data.get('mode', 'generate')
        if mode == 'humanize':
            if not form_data.get('raw_script'):
                return jsonify({'error': 'Raw script is required for humanization mode'}), 400
        else:
            required_fields = ['topic', 'genre']
            missing_fields = [field for field in required_fields if not form_data.get(field)]
            if missing_fields:
                return jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400
        logging.info(f"Processing {mode} request")
        if mode == 'humanize':
            result = humanize_hindi_script(form_data['raw_script'])
        else:
            result = generate_hindi_script(form_data['topic'], form_data['genre'])
        return jsonify({'result': result})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

handler = app
