from flask import Flask, request, Response, make_response
import random
import io
import sys
import time

app = Flask(__name__)

addr = ":39901"
max_clients = 300
clients = {}

def handle_connection(conn):
    conn.close()

    def read_from_conn():
        sys.stdout.write(conn.read())

    def write_to_conn():
        conn.write(sys.stdin.read())

    app.add_url_rule('/conn', 'conn', read_from_conn)
    app.add_url_rule('/conn', 'conn', write_to_conn, methods=['POST'])

def new_id():
    temp = random.randint(0, max_clients)
    while clients.get(temp) is not None:
        temp = random.randint(0, max_clients)
    return temp

def get_id(cookies):
    for cookie in cookies:
        if cookie.name == 'ID':
            return cookie.value
    return ""

@app.route('/', methods=['GET', 'POST'])
def http_handler():
    message = ""
    buff = io.StringIO()

    if request.method == 'GET':
        id = int(get_id(request.cookies))
        if len(clients.get(id, [])) > 0:
            message = clients[id][0]
            clients[id] = clients[id][1:]
        else:
            message = "***NIL***"
        return Response(message)
    elif request.method == 'POST':
        buff.write(request.get_data(as_text=True))
        print(f"\nFrom {request.remote_addr}:\n")
        if buff.getvalue() == "***INIT***":
            id = new_id()
            cli_cmds = list()
            clients[id] = cli_cmds

            resp = make_response("Success")
            resp.set_cookie('ID', str(id))

            print(f"{id} attached")
            print("=> ")
            return resp
        else:
            print(buff.getvalue())
            print("=> ")
            return Response("OK")
    else:
        message = "Bad method"
        return Response(message)

def con_listen_and_serve(addr, handler):
    try:
        app.run(host=addr)
    except Exception as e:
        raise e

def parse_cmd(s):
    print(s)
    if s:
        id = int(s.split()[0])
        cmd = " ".join(s.split()[1:])
        clients.setdefault(id, []).append(cmd)
    else:
        time.sleep(1)

if __name__ == '__main__':
    app.run(debug=True)
    clients = {}

    app.add_url_rule('/', 'http_handler', http_handler)
    con_listen_and_serve(addr, None)

    reader = io.StringIO(sys.stdin.read())
    while True:
        print("=> ")
        s = reader.readline()
        parse_cmd(s)
