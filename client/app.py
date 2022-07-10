
import socket
import threading
import tkinter as tk
from tkinter import ttk
from board import Board
from topPanel import TopPanel
from leaderBoard import LeaderBoard
from mainmenu import MainMenu
from toolbox import Toolbox
from chat import Chat
import pickle

FORMAT = "utf-8"
HEADERSIZE = 10

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.withdraw()
		MainMenu(self)	
		self.name = None
		self.isDrawing = False
		self.scores = None
		self.players = None
		self.inGame = False
		self.gameOver = False
		self.roundID = None
		self.word = ""
		self.color = (0,0,0)
		self.rowconfigure(0, weight=1)
		self.rowconfigure(1, weight=10)
		self.rowconfigure(2, weight=1)
		self.leaderBoard = LeaderBoard(self)
		self.topPanel = TopPanel(self)
		self.board = Board(self)
		self.toolbox = Toolbox(self)
		self.chat = Chat(self)
		

	def connectServer(self):
		PORT = 80
		SERVER = socket.gethostname()
		ADDRESS = (SERVER, PORT)
		FORMAT = "utf-8"
		print (f'Adress: {ADDRESS}')
		# Create a new client socket
		# and connect to the server
		self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.client.connect(ADDRESS)

	def parse_msg(self,msg_dict):
		print (f'Message Recieved to client {msg_dict}')
		if -1 in msg_dict.keys():
			print (f'Sending Name {self.name}')
			self.sendMessage(self.name,-1)

		if -2 in msg_dict.keys():
			print (f'Game Started')
			self.inGame = True

		if 0 in msg_dict.keys():
			self.chat.textChat.config(state=tk.NORMAL)
			self.chat.textChat.insert(tk.END,msg_dict[0]+"\n\n")
			self.chat.textChat.config(state=tk.DISABLED)
			self.chat.textChat.see(tk.END)
		if 1 in msg_dict.keys():
			if msg_dict[1] == True:
				print (f'Player {self.name} is Drawing')
				self.isDrawing = True
			else:
				self.isDrawing = False
		if 2 in msg_dict.keys():
			if not self.isDrawing:
				print (f'Add Pixel: {msg_dict[2]}')
				col,row = msg_dict[2]
				self.board.draw_remote(col,row)
		if 3 in msg_dict.keys():
			if not self.isDrawing:
				print (f'Changing Color: {msg_dict[3]}')
				self.color = msg_dict[3]
		if 4 in msg_dict.keys():
			print (f'Updating Scores: {msg_dict[4]}')
			self.scores = msg_dict[4]
			self.leaderBoard.draw()

		if 5 in msg_dict.keys():
			print (f'Updating Player List: {msg_dict[5]}')
			self.players = msg_dict[5]
			self.leaderBoard.draw()

		if 6 in msg_dict.keys():
			print (f'Updating Round ID: {msg_dict[6]}')
			self.roundID = msg_dict[6]
			self.topPanel.draw()

		if 7 in msg_dict.keys():
			# print (f'Updating timer: {msg_dict[7]}')
			self.topPanel.drawTimer(msg_dict[7])

		if 8 in msg_dict.keys():
			print (f'Updating word: {msg_dict[8]}')
			self.word = msg_dict[8]

		if 9 in msg_dict.keys():
			print (f'Game Over: {msg_dict[9]}')
			self.inGame = False
			self.gameOver = True
			self.topPanel.draw()


	def receive(self):
		full_msg = b''
		new_msg = True

		while True:
			try:
				
				message = self.client.recv(HEADERSIZE)
				if new_msg and message:
					msglen = int(message)
					new_msg = False
				while not new_msg:
					message = self.client.recv(msglen-len(full_msg))
					full_msg += message
					print (f'current msg: {full_msg}')
					print (f'Msg length: {len(full_msg)} out of {msglen}')

					if len(full_msg) == msglen:
						msg_dict = pickle.loads(full_msg)
						self.parse_msg(msg_dict)
						new_msg = True
						full_msg = b""
				


			except Exception as e:
				# an error will be printed on the command line or console if there's an error
				print(f'An error occurred: {e}')
				self.client.close()
				break

	def sendMessage(self,msg, msgType = 0 ):
		msg_dict = pickle.dumps({msgType:msg})
		msg_dict = bytes(f"{len(msg_dict):<{HEADERSIZE}}", FORMAT)+msg_dict
		print (f'Sending Dict : {msg_dict}')
		self.client.sendall(msg_dict)
			


app = App()

def on_closing():
	
	app.client.shutdown(2)
	print (f'Closing Connection on Client: ({app.client}')
	app.client.close()
	app.destroy()

app.protocol("WM_DELETE_WINDOW", on_closing)


app.mainloop()		