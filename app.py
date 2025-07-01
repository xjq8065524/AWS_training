# © The Chancellor, Masters and Scholars of The University of Oxford. All rights reserved

from flask import Flask, render_template, send_from_directory, request, jsonify
import os
import boto3
import uuid
import subprocess

app = Flask(__name__, template_folder=".")

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), filename)

@app.route('/api/execute', methods=['POST'])
def execute():
    data = request.json
    code = data.get('code')
    is_cli = data.get('is_cli', False)
    
    try:
        if is_cli:
            result = subprocess.run(code, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return jsonify({'success': True, 'output': result.stdout})
            else:
                return jsonify({'success': False, 'error': result.stderr})
        else:
            exec(code, {'boto3': boto3, 'uuid': uuid})
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

