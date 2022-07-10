import tkinter as tk
from tkinter import ttk

class LeaderBoard(ttk.Frame):
	def __init__(self,container):
		ttk.Frame.__init__(self,master = container)
		s = ttk.Style()
		# s.configure('TFrame', background='green')
		s.configure('Frame1.TFrame', background='red')

		self.container = container
		self.configure(style='Frame1.TFrame')
		
		self.padding = 50
		self.MARGIN = 20
		# self.WIDTH = 40

		
		self.grid(column=0, row=1, rowspan=2,sticky=tk.N+tk.S, padx = 10, pady = 10)
		self.canvas = tk.Canvas(self,bg = 'pink')
		self.canvas.pack(fill=tk.BOTH, side = tk.TOP, expand = True, padx = 10, pady = 10)
		self.draw()

	# def findXCenter(self, canvas : tk.Canvas, item):
	# 	coords = canvas.bbox(item)
	# 	print (f' canvas width : {canvas.winfo_width()} , text width {(coords[2] - coords[0])}')
	# 	xOffset = (canvas.winfo_width()/2) - ((coords[2] - coords[0]) / 2)
	# 	print (f'Moving offst: {xOffset}')
	# 	return xOffset

	def draw (self):
		self.canvas.delete("all")
		self.canvas.create_text(145, self.MARGIN, text="Leader Board", fill="black", font=('Helvetica 15 bold'),anchor="nw")
		# xOffset = self.findXCenter(self.canvas, header)
		# self.canvas.move(header, xOffset, 0)
		print (f'leaderboard, Ingame: {self.container.inGame}, scores : {self.container.scores}')
		if not self.container.inGame and self.container.players: 
			print (f'Drawing leaderboard players')
			for c,player in enumerate (self.container.players):
				self.canvas.create_text(self.padding, self.MARGIN+60+self.padding*(c+1), text=f"{player}", fill="black", font=('Helvetica 15 bold'),anchor="w")
		elif self.container.inGame and self.container.scores:
			print (f'Drawing leaderboard scores')
			for c,player in enumerate (self.container.scores.keys()):
				self.canvas.create_text(self.padding, self.MARGIN+60+self.padding*(c+1), text=f"{player}:    {self.container.scores[player]}", fill="black", font=('Helvetica 15 bold'),anchor="w")