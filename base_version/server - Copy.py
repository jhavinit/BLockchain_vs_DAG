# first of all import the socket library 
import socket			 
list1 = [10,11]
# next create a socket object
s = socket.socket()
z = socket.socket()
print ("Socket successfully created") 
s.bind(('', 12345))
z.bind(('', 12347))
#print (("socket binded to %s") %(port)) 

# put the socket into listening mode 
s.listen(5)
z.listen(5)
print ("socket is listening")			

# a forever loop until we interrupt it or 
# an error occurs 
#while True:
c, addr = s.accept()
c.send(b'Thank you for connecting')
print ('Got connection from', addr)
print (c.recv(4096))
if c.recv(4096) == b'a':
    list1.append(12)
    print (list1)
y,addr1 = z.accept()
y.send(b'Thank you for connecting')
print ('Got connection from', addr1)
print (y.recv(4096))
if y.recv(4096) == b'a':
    list1.append(13)
    print (list1)
# send a thank you message to the client.
# Close the connection with the client 
c.close()
y.close()
