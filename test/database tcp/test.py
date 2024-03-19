import socket
import time

def connect_to_server(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((ip, port))
            print(f"Connected to server at {ip}:{port}")
            
            # Simulate sending a message to the server after connecting
            message = "Hello from the agent!"
            s.sendall(message.encode())
            print(f"Sent to server: {message}")

            # Wait for and print the response from the server
            response = s.recv(1024).decode()
            print(f"Received from server: {response}")

        except Exception as e:
            print(f"Failed to connect to server: {e}")

if __name__ == "__main__":
    # Specify the IP address and port of the server you wish to connect to
    server_ip = "127.0.0.1"
    server_port = 6565

    # Attempt to connect to the server
    connect_to_server(server_ip, server_port)

    # For continuous operation or periodic check-ins, consider adding a loop or scheduling mechanism
    # This example is a one-time connection and message exchange
