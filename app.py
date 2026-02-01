#!/usr/bin/env python3
"""
Web UI for Selenium Java to Playwright Converter
Phase 4: Stylize (UI Layer)
"""

import os
from flask import Flask, render_template, request, jsonify
from tools.converter import SeleniumToPlaywrightConverter

app = Flask(__name__)

# Ensure output directory exists
os.makedirs('output', exist_ok=True)

# Global converter instance
converter_ts = SeleniumToPlaywrightConverter('typescript', 'output')
converter_js = SeleniumToPlaywrightConverter('javascript', 'output')


@app.route('/')
def index():
    """Render the main UI."""
    return render_template('index.html')


@app.route('/api/convert', methods=['POST'])
def convert():
    """API endpoint to convert Java code."""
    data = request.json
    java_code = data.get('code', '')
    target_lang = data.get('language', 'typescript')
    
    if not java_code.strip():
        return jsonify({
            'success': False,
            'error': 'No Java code provided'
        })
    
    # Select converter based on target language
    converter = converter_ts if target_lang == 'typescript' else converter_js
    
    # Convert the code
    result = converter.convert(java_code, 'UserInput.java')
    
    return jsonify(result)


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'ollama': check_ollama(),
    })


def check_ollama():
    """Check if Ollama is running."""
    try:
        import ollama
        ollama.list()
        return True
    except:
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("Selenium Java to Playwright Converter")
    print("=" * 60)
    print("Open your browser and go to: http://localhost:5000")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True)
