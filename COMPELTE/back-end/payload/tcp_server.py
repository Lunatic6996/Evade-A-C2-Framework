import socket
import threading
import json
from database import Session, Agent
import requests

# Global dictionary for tracking agent connections
agent_connections = {}

# Fixed port for backend commands
COMMAND_PORT = 62347

def notify_flask_about_agent_connection(agent_id):
    url = 'http://localhost:5002/api/notify-agent-connection'  # Flask app URL
    data = {'agent_id': agent_id}
    try:
        response = requests.post(url, json=data)
        print("Notification sent to Flask app:", response.json())
    except requests.exceptions.RequestException as e:
        print("Failed to notify Flask app:", e)

def handle_agent_connection(conn, addr):
    """Handle connections from agents."""
    with Session() as session:
        while True:
            data = conn.recv(2048).decode()
            if not data:
                break
            agent_id = data  # Assuming the agent sends its ID first
            agent = session.query(Agent).filter_by(agent_id=agent_id).first()
            if agent:
                print(f"Agent {agent_id} recognized. Connection established.")
                agent_connections[agent_id] = conn
                notify_flask_about_agent_connection(agent_id)
            else:
                print(f"Unrecognized agent ID: {agent_id}")

def handle_command_connection(conn, addr):
    """Handle command connections from the backend."""
    while True:
        data = conn.recv(2048).decode()
        if not data:
            break
        try:
            command_info = json.loads(data)
            agent_id = command_info['agent_id']
            command = command_info['command']
            if agent_id in agent_connections:
                agent_conn = agent_connections[agent_id]
                agent_conn.sendall(command.encode())
                print(f"Command '{command}' sent to agent {agent_id}.")
            else:
                print(f"Agent {agent_id} is not connected.")
        except json.JSONDecodeError:
            print("Malformed command data received.")

def start_agent_listener(ip, port):
    """Listen for agent connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Listening for agent connections on {ip}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_agent_connection, args=(conn, addr)).start()

def start_command_listener(ip, port=COMMAND_PORT):
    """Listen for backend command connections."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"Listening for backend command connections on {ip}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_command_connection, args=(conn, addr)).start()

def start_tcp_server(ip, agent_port):
    """Start the TCP server for agent and command connections."""
    # Start listener for agents
    threading.Thread(target=start_agent_listener, args=(ip, agent_port)).start()
    # Start listener for backend commands
    threading.Thread(target=start_command_listener, args=(ip,COMMAND_PORT)).start()

