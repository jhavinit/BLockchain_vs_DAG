# Import socket module 
import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12347              
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port))

s.send(b'hello world7');
inp = input("enter:")
s.send(b'a');
  
# receive data from the server 
print (s.recv(1024)) 

# close the connection 
s.close()
