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
    """Handle connections from agents and command responses."""
    print(f"Got the connection from {addr}")
    with Session() as session:
        while True:
            data = conn.recv(2048).decode()
            if not data:
                break

            try:
                # Attempt to parse the data as JSON
                data_json = json.loads(data)
                agent_id = data_json.get('agent_id')
                command_response = data_json.get('response')
                print(f"Command response from {agent_id}: {command_response}")
                
                # Here, you might want to forward this response to the frontend or handle it as needed.
                # Ensure you have logic here to properly manage and use the command response.

            except json.JSONDecodeError:
                # If JSON parsing fails, treat data as the agent ID (plain text)
                agent_id = data
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
                # Send the command to the agent
                agent_conn.sendall(command.encode())
                # Wait for the response from the agent
                response = agent_conn.recv(2048).decode()
                # Send the response back to the backend
                conn.sendall(response.encode())
                print(f"Response from agent {agent_id} relayed back to backend.")
            else:
                print(f"Agent {agent_id} is not connected. Unable to send command.")
                conn.sendall(f"Agent {agent_id} is not connected.".encode())
        except json.JSONDecodeError:
            print("Malformed command data received.")
            conn.sendall("Malformed command data received.".encode())


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

