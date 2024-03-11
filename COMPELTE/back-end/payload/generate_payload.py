from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
import uuid
import logging

from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory for generated payloads
payload_dir = 'generated_payloads'
os.makedirs(payload_dir, exist_ok=True)

@app.route('/download/<filename>')
def download_payload(filename):
    try:
        return send_from_directory(directory=payload_dir, filename=filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404


@app.route('/api/generate-payload', methods=['POST'])
def generate_payload():
    logging.info("Generating payload...")
    print("hit hit hit")
    print("payload")
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ["name", "lhost", "lport", "type", "protocol"]):
            logging.error("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        name, lhost, lport, payload_type, protocol = data["name"], data["lhost"], data["lport"], data["type"], data["protocol"]

        if payload_type not in ['.py', '.exe'] or protocol not in ['tcp', 'http', 'https']:
            logging.error("Invalid type or protocol specified")
            return jsonify({"error": "Invalid type or protocol specified"}), 400

        # Assuming templates are Python files with placeholders for lhost and lport
        #template_file = f'templates/{protocol}_agent_template.py'
        template_file = os.path.join(BASE_DIR, "templates", f"{protocol}_agent_template.py")
        if not os.path.exists(template_file):
            logging.error("Template file does not exist")
            return jsonify({"error": "Template file does not exist"}), 400

        with open(template_file, 'r') as f:
            template_content = f.read()

        # Replace placeholders in template
        filled_content = template_content.format(lhost=lhost, lport=lport)

        # Create a temporary file for the filled template
        temp_filename = f"{name}_{str(uuid.uuid4())}.py"
        temp_filepath = os.path.join(payload_dir, temp_filename)
        with open(temp_filepath, 'w') as temp_file:
            temp_file.write(filled_content)

        if payload_type == '.exe':
            # Convert .py to .exe using PyInstaller
            subprocess.run(['pyinstaller', '--onefile', '--distpath', payload_dir, temp_filepath], check=True)
            # Assuming PyInstaller creates .exe with the same base filename
            exe_filename = f"{name}.exe"
            final_path = os.path.join(payload_dir, exe_filename)
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)  # Clean up temporary .py file
        else:
            final_path = temp_filepath

        download_url = request.url_root + 'download/' + os.path.basename(final_path)
        return jsonify({"message": "Payload generated successfully", "downloadUrl": download_url})

    except Exception as e:
        logging.exception("Error generating payload")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)

