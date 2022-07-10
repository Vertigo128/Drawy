import socket
import pickle
import threading
from player import Player

# Choose a port that is free
PORT = 80
HEADERSIZE = 10
# An IPv4 address is obtained
# for the server.
SERVER = socket.gethostname()
print (SERVER)
# Address is stored as a tuple
ADDRESS = (SERVER, PORT)
print (f'Adress: {ADDRESS}')
# the format in which encoding
# and decoding will occur
FORMAT = "utf-8"

class Network(object):
	def __init__(self, main) -> None:
		
		self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #create socket
		self.server.bind(ADDRESS) # bind the address of the server to the socket
		self.main = main
		self.game = None
		

	
	def startChat(self):
		'''
		function to start the connection
		'''
		print("server is working on " + SERVER)
	
		self.server.listen() # listening for connections
    
		while True:
			conn, addr = self.server.accept()

			self.sendMessage(conn,"NAME",-1)

			# msg_dict = pickle.dumps({-1:"NAME"})
			# msg_header = bytes(f"{len(msg_dict):<{HEADERSIZE}}", FORMAT)

			# msg_dict = bytes(f"{len(msg_dict):<{HEADERSIZE}}", FORMAT)+msg_dict

			# conn.send(msg_header)
			# conn.send(msg_dict)
		
			name = self.read_msg_dict(conn).get(-1)
			
			self.main.playerList.append (Player(conn,name,self.main.playerID))
			self.main.playerID += 1

		
			# append the name and client
			# to the respective list
			self.main.names.append(name)
			self.main.clients.append(conn)
		
			print(f"Name is :{name}")
		
			# broadcast message
			self.broadcastMessage(f"{name} has joined the chat",0)
			self.sendMessage (conn, 'Connection successful!', 0)

			self.main.handleQueue()
		
			# Start the handling thread
			thread = threading.Thread(target=self.comm,
						args=(conn, addr))
			thread.start()
		
			# no. of clients connected
			# to the server
			print(f"active connections {threading.activeCount()-1}")

	def read_msg_dict(self,conn):
        
		'''
		Read next message and parse it to dictionary
		'''

		msg_not_done = True
		full_msg = b''
		new_msg = True
	
		while msg_not_done:    
			message = conn.recv(16) # receive message
			if not message: break
		
			if new_msg:
				msglen = int(message[:HEADERSIZE])
				new_msg = False
			
			full_msg += message
			print (f'Recieveing msg Server.. {full_msg}')
			if len(full_msg)-HEADERSIZE == msglen:
				
				msg_dict = pickle.loads(full_msg[HEADERSIZE:])
				print (f'Finished reading : {msg_dict}')
				return (msg_dict)


	def parse_msg(self, msg_dict):
		'''
		act based on the incoming message dictionary
		'''
		print (f'Message Recieved to Server {msg_dict}')
		if msg_dict.get(0): #code 0 for chat update
			msg = msg_dict[0]
			self.broadcastMessage(msg, 0)
			if self.game:	
				player = self.game.getPlayerFromMessage(msg)
				guess =  msg[msg.find(":") + 2 :]
				self.game.round.guess(player,guess)

		if msg_dict.get(2): #code 2 for update pixel
			self.broadcastMessage(msg_dict[2], 2)
			print (f'Sending Pixel {msg_dict[2]}')
		if msg_dict.get(3): #code changing current color
			self.broadcastMessage(msg_dict[3], 3)
			print (f'Changing to Color: {msg_dict[3]}')



	def comm(self,conn, addr):
		'''
		Thread to keep reading messeges and broadcast 
		'''
	
		print(f"new connection {addr}")
		connected = True

		while connected:

			msg_dict = self.read_msg_dict(conn)
			if not msg_dict:break
			self.parse_msg(msg_dict)
	
			# close the connection
		self.main.clients.remove(conn)
		conn.close()
    
# method for broadcasting
# messages to the each clients
 
 
	def broadcastMessage(self,msg, msgType = 0):
		'''
		Send message to all clients
		the message format is dict {Code : value}
		'''
		print (f'sending to all Clients, msg: {msg}, type: {msgType}')
		msg_dict = pickle.dumps({msgType:msg})
		msg_header = bytes(f"{len(msg_dict):<{HEADERSIZE}}", FORMAT)

		print (f'Sending Dict : {msg_dict}')
		for client in self.main.clients:
			client.sendall(msg_header)
			client.sendall(msg_dict)
    

	def sendMessage(self,client:socket, msg, msgType = 0 ):
		'''
		Send message to specific client
		the message format is dict {Code : value}
		'''

		print (f'sending to {client}, msg: {msg}, type: {msgType}')
		msg_dict = pickle.dumps({msgType:msg})
		msg_header = bytes(f"{len(msg_dict):<{HEADERSIZE}}", FORMAT)
		print (f'Sending Dict : {msg_dict}')
		client.sendall(msg_header)
		client.sendall(msg_dict)
	