from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

HOST_NAME = '127.0.0.1'
PORT_NUMBER = 80

class MyHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def do_GET(self):
        self._set_response()
        user_input = input("Enter a command to send to the client: ")
        self.wfile.write(user_input.encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # Decode the URL-encoded data and remove '+' symbols
        decoded_data = urllib.parse.unquote(post_data.decode('utf-8')).replace('+', '')

        response_data = f"Output:\n{decoded_data}"

        self._set_response()
        self.wfile.write(response_data.encode('utf-8'))
        print(response_data)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        print(f"[*] Server started on http://{HOST_NAME}:{PORT_NUMBER}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        httpd.server_close()
