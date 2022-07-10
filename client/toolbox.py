import tkinter as tk
from tkinter import ttk


class Toolbox(ttk.Frame):
	
	def __init__(self,container):
		ttk.Frame.__init__(self,container)
		self.container = container
		self.colors = ['red','green', 'blue', 'black', 'white']
		self.SIDE = 20
		self.padding = 8
		self.MARGIN = 20
		# self['padding'] = self.padding
		self['width'] = (self.SIDE+ self.padding)*len(self.colors) + self.MARGIN*2
		self['height'] = self.SIDE + self.MARGIN*2
		self.grid(column=1, row=2)
		
		self.canvas = tk.Canvas(self, width=(self.SIDE+self.MARGIN)*len(self.colors), height=self.SIDE+ self.MARGIN*2)
		self.canvas.pack(fill=tk.BOTH, side = tk.LEFT)
		self.draw()
		self.canvas.bind('<Button-1>', self.get_color)



	def draw (self):
		for i,color in enumerate(self.colors):
			x0 = self.MARGIN + i*(self.SIDE+self.padding)
			y0 = self.MARGIN
			x1 = x0 + self.SIDE
			y1 = y0 + self.SIDE
			self.canvas.create_rectangle(x0,y0,x1,y1,fill= color)

	def get_color(self,event):
		for i,color in enumerate(self.colors):
			x0 = self.MARGIN + i*(self.SIDE+self.padding)
			y0 = self.MARGIN
			x1 = x0 + self.SIDE
			y1 = y0 + self.SIDE
			if x1>=event.x>=x0 and y1>=event.y>=y0:
				self.container.color = color
				print (f'New Color : {color}')
				self.container.sendMessage(color, 3)

	# def clearBoard(self):
	# 	self.container.client.close()
	# 	# self.container.board.clearBoard()
	# 	# self.container.board.canvas.update()
	# 	# self.container.board.canvas.update_idletasks()

