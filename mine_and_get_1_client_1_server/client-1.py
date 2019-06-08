import socket
import json
s = socket.socket()            
s.connect(('127.0.0.1', 12345))
while 1:
    ch = input("enter choice:")
    if ch == 'a':
        s.send(b'a')
    if ch == 'c':
        s.send(b'c') 
    b = b''
    tmp = s.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8'))     
    print(d) 
s.close()


 
