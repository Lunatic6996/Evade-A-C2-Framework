import socket
import threading
from database import Session, Agent  # Import the Session for DB operations
import requests

def notify_flask_about_agent_connection(agent_id):
    url = 'http://localhost:5002/api/notify-agent-connection'  # Flask app URL
    data = {'agent_id': agent_id}
    try:
        response = requests.post(url, json=data)
        print("Notification sent to Flask app:", response.json())
    except requests.exceptions.RequestException as e:
        print("Failed to notify Flask app:", e)

def handle_client(conn, addr):
    print(f"Connected by {addr}")
    session = Session()  # Create a new session for this thread
    try:
        while True:
            data = conn.recv(2048).decode()
            agent_id=data
            if not data:
                break
            print(data)
            # Example of querying the database independent of Flask app context
            agent = session.query(Agent).filter_by(agent_id=agent_id).first()
            if agent:
                print(f"Agent {agent_id} recognized.")
                notify_flask_about_agent_connection(agent_id)
            else:
                print(f"Agent {agent_id} not recognized.")
            #conn.sendall(data)  # Echo back the received data for simplicity
    finally:
        session.close()  # Make sure to close the session

def start_tcp_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ip, port))
        s.listen()
        print(f"TCP Server listening on {ip}:{port}")
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
