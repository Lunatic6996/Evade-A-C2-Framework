import socket

ip = '127.0.0.1'
port = 6666

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip, port))

while True:
    ola=input("Enter the message you want to send")
    cs.send(ola.encode())
    hola=cs.recv(1024).decode()
    print(hola)


