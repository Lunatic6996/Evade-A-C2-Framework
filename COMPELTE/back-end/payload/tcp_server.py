import socket
import requests
import threading
import json
import os
from database import Session, Agent  # Assuming the existence of a database handling module

# Global dictionary to keep track of agent connections
agent_connections = {}
backend_connection = None
# Fixed port for receiving commands from the backend
COMMAND_PORT = 62347

def notify_flask_about_agent_connection(agent_id):
    """Notify the Flask application about an agent connection."""
    url = 'http://localhost:5002/api/notify-agent-connection'
    data = {'agent_id': agent_id}
    try:
        requests.post(url, json=data)
        print(f"Agent {agent_id} connected and notified to Flask app.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to notify Flask app: {e}")

def handle_agent_connection(conn, addr):
    '''Handles connection with agents.'''
    try:
        # Receive agent ID
        agent_id = conn.recv(1024).decode()
        if agent_id:
            with Session() as session:
                # Check if the agent ID exists in the database
                agent = session.query(Agent).filter_by(agent_id=agent_id).first()
                if agent:
                    print(f"Agent {agent_id} recognized.")
                    agent_connections[agent_id] = conn
                    notify_flask_about_agent_connection(agent_id)
                else:
                    print(f"Unrecognized agent: {agent_id}. Connection refused.")
                    conn.close()
        else:
            print("Agent ID not received.")
            conn.close()
    except Exception as e:
        print(f"Error handling agent connection: {e}")
        conn.close()

def handle_agent_commands(conn, agent_id):
    '''Processes commands received for agents from backend.'''
    try:
        while True:
            command = conn.recv(2048).decode().strip()
            if not command:
                continue

            # Check if the command is a special command like download, upload, or cd
            if command.startswith(('download', 'upload', 'cd')):
                handle_special_command(conn, agent_id, command)
            else:
                handle_normal_command(conn, agent_id, command)

    except Exception as e:
        print(f"Error processing agent commands: {e}")
        conn.close()

def handle_special_command(conn, agent_id, command):
    '''Handles special commands like download, upload, and cd.'''
    try:
        # Split the command to get the action and optional parameters
        cmd_parts = command.split(" ", 1)
        action = cmd_parts[0]

        if action == 'download':
            filename = cmd_parts[1] if len(cmd_parts) > 1 else ''
            handle_download(conn, filename)
        elif action == 'upload':
            filename = cmd_parts[1] if len(cmd_parts) > 1 else ''
            handle_upload(conn, filename)
        elif action == 'cd':
            directory = cmd_parts[1] if len(cmd_parts) > 1 else ''
            handle_change_directory(conn, directory)
        else:
            # Unsupported special command
            response = f"Unsupported special command: {action}"
            conn.send(response.encode())
    except Exception as e:
        print(f"Error handling special command: {e}")
        conn.close()

def handle_download(conn, filename):
    """Handles download command."""
    try:
        if os.path.isfile(filename):
            file_size = os.path.getsize(filename)
            conn.send(str(file_size).encode())

            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(2048)
                    if not chunk:
                        break
                    conn.send(chunk)
        elif os.path.isdir(filename):
            conn.send(b"Is a directory")
        else:
            conn.send(b"File does not exist")
    except Exception as e:
        response = f"Error during download: {str(e)}"
        conn.send(response.encode())

def handle_upload(conn, filename):
    """Handles upload command."""
    try:
        # Receive file size from agent
        file_size = int(conn.recv(1024).decode())

        # Confirm readiness to receive file
        conn.send(b"Ready for upload")

        # Receive file data
        received_size = 0
        with open(filename, 'wb') as f:
            while received_size < file_size:
                chunk = conn.recv(2048)
                f.write(chunk)
                received_size += len(chunk)

        # Notify agent about successful upload
        conn.send(b"File Upload Successful.")
    except Exception as e:
        response = f"Error during upload: {str(e)}"
        conn.send(response.encode())

def handle_change_directory(conn, directory):
    """Handles change directory command."""
    try:
        if directory:
            os.chdir(directory)
            response = f"Changed directory to {os.getcwd()}"
        else:
            response = "No directory specified"
    except Exception as e:
        response = f"Error changing directory: {str(e)}"
    conn.send(response.encode())

def handle_normal_command(conn, agent_id, command):
    '''Handles normal commands.'''
    # Send the command to the appropriate agent
    send_command_to_agent(agent_id, command)

def send_command_to_agent(agent_id, command):
    '''Forwards command to the appropriate agent.'''
    try:
        agent_conn = agent_connections.get(agent_id)
        if agent_conn:
            agent_conn.send(command.encode())
            print(f"Command sent to Agent {agent_id}: {command}")

            # Receive response from agent
            receive_agent_response(agent_conn, agent_id)
        else:
            print(f"No active connection found for Agent {agent_id}")
    except Exception as e:
        print(f"Error sending command to Agent {agent_id}: {e}")

def start_agent_listener(ip, port):
    """Listens for new agent connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Listening for agent connections on {ip}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_agent_connection, args=(conn, addr)).start()

def start_tcp_server(ip, agent_port):
    """Start the TCP server."""
    # Start listener for agents
    threading.Thread(target=start_agent_listener, args=(ip, agent_port)).start()

    # Start listener for backend commands
    threading.Thread(target=start_command_listener, args=(ip, COMMAND_PORT)).start()

def start_command_listener(ip, port):
    """Listens for command dispatches from the backend."""
    global backend_connection 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Listening for command connections on {ip}:{port}")
        while True:
            conn, addr = s.accept()
            backend_connection = conn
            threading.Thread(target=handle_command_connection, args=(conn, addr)).start()

def receive_agent_response(conn, agent_id):
    '''Receives response from agent for the command sent.'''
    try:
        response = conn.recv(2048).decode().strip()
        if response:
            print(f"Response received from Agent {agent_id}: {response}")
            # Here, you can process the response as needed (e.g., send it back to the backend)
            send_result_back_to_backend(response, agent_id)
        else:
            print(f"No response received from Agent {agent_id}")
    except Exception as e:
        print(f"Error receiving response from Agent {agent_id}: {e}")

def send_result_back_to_backend(response, agent_id):
    global backend_connection  # Access the global variable
    if backend_connection:
        # Send the response back to the backend server
        backend_connection.send(json.dumps({"agent_id": agent_id, "response": response}).encode())
    else:
        print("Backend connection is not established.")

def handle_command_connection(conn, addr):
    """Handles connections for receiving commands from the backend."""
    try:
        command_data = conn.recv(1024).decode()
        if command_data:
            command_json = json.loads(command_data)
            agent_id = command_json.get('agent_id')
            command = command_json.get('command')
            if agent_id and command:
                send_command_to_agent(agent_id, command)
            else:
                print("Incomplete command data received from backend.")
        else:
            print("No command data received from backend.")
    except Exception as e:
        print(f"Error handling command connection: {e}")
        conn.close()
