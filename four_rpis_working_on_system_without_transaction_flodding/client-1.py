import socket
import json
s = socket.socket()            
s.connect(('127.0.0.1', 12345))
s.send(b'cl')
while 1:
    ch = input("enter choice:")
    if ch == 'a':
        s.send(b'a')
    if ch == 'b':
        s.send(b'b')
    if ch == 'c':
        s.send(b'c')
        s.send(b'private_key_node_1')
        s.send(b'private_key_node_2')
        s.send(b'1000')
    if ch == 'd':
        s.send(b'd')
        s.send(b'12346')
        s.send(b'12347')
        s.send(b'12348')
    if ch == 'm':
        s.send(b'm')  
    b = b''
    tmp = s.recv(1048576)
    b += tmp
    d = json.loads(b.decode('utf-8'))     
    print(d) 
s.close()


 
