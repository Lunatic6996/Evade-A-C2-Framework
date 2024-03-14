'''
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
        required_fields = ["name", "lhost", "lport", "type", "protocol", "persistence"]
        if not data or not all(key in data for key in required_fields):
            logging.error("Missing required fields")
            return jsonify({"error": "Missing required fields"}), 400

        name, lhost, lport, payload_type, protocol, persistence = (
            data["name"], 
            data["lhost"], 
            data["lport"], 
            data["type"], 
            data["protocol"], 
            data["persistence"]
        )

        # For now, handling tcp template. Adjustments for http/https will be similar
        if payload_type not in ['.py', '.exe'] or protocol not in ['tcp','http','https']:
            logging.error("Invalid type or protocol specified")
            return jsonify({"error": "Invalid type or protocol specified"}), 400

        template_file = os.path.join(template_dir, "templates", f"{protocol}_agent_template.py")
        if not os.path.exists(template_file):
            logging.error("Template file does not exist")
            return jsonify({"error": "Template file does not exist"}), 400

        with open(template_file, 'r') as f:
            template_content = f.read()

        # Extract content within the triple quotes
        start_index = template_content.find('"""') + 3
        end_index = template_content.rfind('"""')
        payload_content = template_content[start_index:end_index]

        # Perform placeholder replacements, ensuring lhost is enclosed in single quotes
        modified_content = payload_content.replace("{lhost}", f"{lhost}").replace("{lport}", str(lport))

        unique_id = str(uuid.uuid4())
        temp_filename = f"{name}_{unique_id}.{payload_type.strip('.')}"
        temp_filepath = os.path.join(payload_dir, temp_filename)

        # Write the modified content to the output file
        with open(temp_filepath, 'w') as temp_file:
            temp_file.write(modified_content)

        final_path = temp_filepath
        if payload_type == '.exe':
            exe_name = f"{name}_{unique_id}"
            # Ensure pyinstaller outputs the .exe directly in the desired directory
            subprocess.run(['pyinstaller', '--onefile', '--distpath', payload_dir, '--name', exe_name, temp_filepath], check=True)
            # The expected .exe file path
            final_path = os.path.join(payload_dir, exe_name + '.exe')
            if not os.path.exists(final_path):
                logging.error(f"Expected .exe file not found: {final_path}")
                return jsonify({"error": "Failed to generate .exe file"}), 500


        download_url = request.url_root + 'download/' + os.path.basename(final_path)
        return jsonify({"message": "Payload generated successfully", "downloadUrl": download_url})

    except Exception as e:
        logging.exception("Error generating payload")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)
    
'''


from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import uuid
import os
import logging
# Import agent template functions
from agent_templates import tcp_agent_template, http_agent_template, https_agent_template

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = 'E:\\Github\\Repos\\Evade-A-C2-Framework\\COMPELTE\\generated_payloads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

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
    data = request.get_json()
    print(data)
    required_fields = ["name", "lhost", "lport", "type", "protocol", "persistence"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    print("----------------------------------------------")
    print("Sabai chha")
    print("----------------------------------------------")

    # Extract parameters
    name, lhost, lport, payload_type, protocol, persistence = (
        data["name"], data["lhost"], data["lport"], data["type"], data["protocol"], data["persistence"]
    )

    userAgent = data.get("userAgent", "")
    sleepTimer = data.get("sleepTimer", "")
    print("----------------------------------------------")
    print(name, lhost, lport, payload_type, protocol, persistence, userAgent, sleepTimer )
    print("----------------------------------------------")

    # Choose the appropriate template function and prepare parameters
    if protocol == "tcp":
        agent_code = tcp_agent_template(lhost=lhost, lport=lport, persistence=persistence)
    elif protocol == "http":
        try:
            print(f"Handling {protocol.upper()} protocol")
            print(f"User-Agent: {data.get('userAgent', 'Not provided')}, Sleep Timer: {data.get('sleepTimer', 'Not provided')}")
            
            if not all(param in data for param in ["userAgent", "sleepTimer"]):
                return jsonify({"error": "Missing required HTTP fields"}), 400
            print("----------------------------------------------")
            print("Sabai chha data haru")
            print("----------------------------------------------")
            # Use the HTTP agent template function
            agent_code = http_agent_template(
                lhost=lhost, 
                lport=lport, 
                persistence=persistence, 
                userAgent=userAgent, 
                sleepTimer=sleepTimer
            )

            print(agent_code)
        except Exception as e:
            # Log the exception or print for debugging
            print(f"Error generating HTTP agent: {e}")
            # Return a response indicating an internal error occurred
            return jsonify({"error": "An error occurred while generating the HTTP agent", "details": str(e)}), 500

    elif protocol == "https":
        print(f"Handling {protocol.upper()} protocol")
        print(f"User-Agent: {data.get('userAgent', 'Not provided')}, Sleep Timer: {data.get('sleepTimer', 'Not provided')}")
        
        if not all(param in data for param in ["userAgent", "sleepTimer"]):
            return jsonify({"error": "Missing required HTTPS fields"}), 400

        # Use the HTTPS agent template function
        agent_code = https_agent_template(
            lhost=lhost, 
            lport=lport, 
            persistence=persistence, 
            userAgent=data['userAgent'], 
            sleepTimer=data['sleepTimer']
        )

    else:
        return jsonify({"error": "Invalid protocol specified"}), 400



    print("----------------------------------------------")
    print("Filename ma pugyo")
    print("----------------------------------------------")
    # Save the generated code to a file
    filename = f"{name}_{str(uuid.uuid4())}{'.py' if payload_type == '.py' else '.exe'}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'w') as file:
        file.write(agent_code)

    # Compile to .exe if needed
    if payload_type == '.exe':
        try:
            subprocess.run(['pyinstaller', '--onefile', '--distpath', app.config['UPLOAD_FOLDER'], '--name', filename, filepath], check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to compile .exe file: {e}")
            return jsonify({"error": "Failed to compile .exe file"}), 500

    download_url = f"http://{request.host}/download/{filename}"
    return jsonify({"message": "Payload generated successfully", "downloadUrl": download_url})

if __name__ == "__main__":
    app.run(debug=True, port=5002)
