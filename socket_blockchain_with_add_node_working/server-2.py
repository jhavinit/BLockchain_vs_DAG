
# Module 2 - Create a Cryptocurrency

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/
# requests==2.18.4: pip install requests==2.18.4

# Importing the libraries
import datetime
import hashlib
import json
#from flask import Flask, jsonify, request
#import requests
from uuid import uuid4
from urllib.parse import urlparse

# first of all import the socket library 
import socket

from _thread import *
import threading


# next create a socket object 
s = socket.socket()		 
print ("Socket successfully created")

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12346				

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))		 
print (("socket binded to %s") %(port)) 

# put the socket into listening mode 
s.listen(5)	 
print ("socket is listening")			

# a forever loop until we interrupt it or 
# an error occurs
# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set()
    
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({'sender': sender,
                                  'receiver': receiver,
                                  'amount': amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self, address): 
        self.nodes.add(address)
    '''
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
    '''
            
    def replace_chain(self):
            network = self.nodes
            #print (network)
            longest_chain = None
            max_length = len(self.chain)
            for node in network:
                m = socket.socket()
                m.connect(('127.0.0.1', int(node)))
                m.send(b's')
                b = b''
                tmp = m.recv(1048576)
                b += tmp
                d = json.loads(b.decode('utf-8'))
                print (d)
                chain = d['chain']
                length = d['length']
                #if response.status_code == 200:
                #    length = response.json()['length']
                #    chain = response.json()['chain']
                if length > max_length:
                        max_length = length
                        longest_chain = chain
                m.close()
            if longest_chain:
                self.chain = longest_chain
                return True 
            return False

# Part 2 - Mining our Blockchain

# Creating a Web App
#app = Flask(__name__)

# Creating an address for the node on Port 5000
node_address = str(uuid4()).replace('-', '')

# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
#@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Vinit Jha', amount = 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return response

# Getting the full Blockchain
#@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return response

# Checking if the Blockchain is valid
#@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Adding a new transaction to the Blockchain
#@app.route('/add_transaction', methods = ['POST'])
def add_transaction(sender,reciever,amount):
    #json = request.get_json()
    #transaction_keys = ['sender', 'receiver', 'amount']
    #if not all(key in json for key in transaction_keys):
    #    return 'Some elements of the transaction are missing', 400
    index = blockchain.add_transaction(sender,reciever,amount)
    #response = {'message': f'This transaction will be added to Block {index}'}
    response = {'message':'This transaction will be added to Block'}
    return response

# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
#@app.route('/connect_node', methods = ['POST'])
def connect_node(nodes1):
    #json = request.get_json()
    #nodes = json.get('nodes')
    nodes = nodes1
    #if nodes is None:
    #    return "No node"
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'All the nodes are now connected. The Hadcoin Blockchain now contains the following nodes:'}
    return response

# Replacing the chain by the longest chain if needed
#@app.route('/replace_chain', methods = ['GET'])

def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message': 'The nodes had different chains so the chain was replaced by the longest one.',
                    'new_chain': blockchain.chain}
    else:
        response = {'message': 'All good. The chain is the largest one.',
                    'actual_chain': blockchain.chain}
    return response

def for_server(c):
    a_dict  = get_chain()
    b = json.dumps(a_dict).encode('utf-8')
    c.send(b)
    
def for_client(c):
    while 1:
        var1 = c.recv(4096)
        if var1 == b'a':
            #c.send(b'hello world')
            a_dict  = mine_block()
            b = json.dumps(a_dict).encode('utf-8')
            c.send(b)
            #s.close();
            
        if var1 == b'b':
            #c.send(b'hello world')
            a_dict  = get_chain()
            b = json.dumps(a_dict).encode('utf-8')
            c.send(b)
            
        if var1 == b'c':
            #c.send(b'hello world')
            sender = c.recv(4096).decode('utf-8');
            reciever = c.recv(4096).decode('utf-8');
            amount = c.recv(4096).decode('utf-8');
            a_dict  = add_transaction(sender,reciever,amount)
            b = json.dumps(a_dict).encode('utf-8')
            c.send(b)
        
        if var1 == b'd':
            #c.send(b'hello world')
            mem1 = c.recv(4096).decode('utf-8');
            #mem2 = c.recv(4096).decode('utf-8');
            #mem3 = c.recv(4096).decode('utf-8');
            #mem4 = c.recv(4096).decode('utf-8');
            nodes1 = set();
            nodes1.add(mem1)
            #nodes1.add(mem2)
            #nodes1.add(mem3)
            #nodes1.add(mem4)
            a_dict  = connect_node(nodes1)
            b = json.dumps(a_dict).encode('utf-8')
            c.send(b)
            
        if var1 == b'm':
            #replace chain
            a_dict  = replace_chain()
            b = json.dumps(a_dict).encode('utf-8')
            c.send(b)
            
# Running the app
#app.run(host = '0.0.0.0', port = 5000)
while True: 
    c, addr = s.accept() 
    print('Connected to :', addr[0], ':', addr[1]) 
    if c.recv(4069) == b's':
        print("for_Server")
        start_new_thread(for_server, (c,))
    else:
        print("for_Client")
        start_new_thread(for_client, (c,))
c.close();
