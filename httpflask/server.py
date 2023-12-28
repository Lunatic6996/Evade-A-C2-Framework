from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store the command to be executed by the agent and the output
current_command = {"command": "", "output": ""}

# HTML page for command input and output
@app.route('/', methods=['GET', 'POST'])
def index():
    global current_command

    if request.method == 'POST':
        # If the form is submitted, update the current command
        current_command["command"] = request.form.get('command', '')

    return render_template('index.html', command=current_command["command"], output=current_command["output"])

# Endpoint for the agent to get commands and output
@app.route('/get_command', methods=['GET'])
def get_command():
    global current_command
    return jsonify({'command': current_command["command"], 'output': current_command["output"]})

# Endpoint for the agent to send output back to the server
@app.route('/output', methods=['POST'])
def receive_output():
    global current_command
    output = request.form.get('output', '')
    current_command["output"] = output

    # Notify clients about the updated output using WebSockets
    socketio.emit('output_update', {'output': output})

    return 'Output received successfully'

if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)

