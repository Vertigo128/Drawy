import tkinter as tk
from tkinter import ttk

# class App(tk.Tk):
# 	def __init__(self):
# 		super().__init__()
# 		self.color = (0,0,0)
# 		self.columnconfigure(0, weight=1)
# 		username_label = ttk.Label(self, text="Username:")
# 		username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)


class Board(ttk.Frame):
	
	def __init__(self,container):
		ttk.Frame.__init__(self,container)
		self.container = container
		self.MARGIN = 5
		self.PIXEL_SIZE = 8
		self.ROWS = 70
		self.COLS = 70
		self.WIDTH = self.PIXEL_SIZE*self.COLS
		self.HEIGHT = self.PIXEL_SIZE*self.ROWS
		self.board = [[(255,255,255) for r in range(self.ROWS)] for c in range(self.COLS)]
		self.x = 0
		self.y = 0
		self['padding'] = self.MARGIN
		# self['width'] = self.WIDTH + self.MARGIN*3
		# self['height'] = self.HEIGHT + self.MARGIN*3
		self.grid(column=1, row=1)
		self.canvas = tk.Canvas(self, width=self.WIDTH+self.MARGIN*2, height=self.HEIGHT+ self.MARGIN*2)
		self.canvas.pack(fill=tk.BOTH, side = tk.TOP)
		self.draw()
		self.canvas.bind('<Button-1>', self.click)
		self.canvas.bind('<B1-Motion>', self.click)

		ereaser_icon = tk.PhotoImage(file='.\img\ereaser.png')
		self.clearButton = ttk.Button(self, image=ereaser_icon,text='Clear',compound=tk.LEFT,command = self.clearBoard)
		self.clearButton.pack(side='right', expand=True)

	def _from_rgb(self,rgb):
		"""translates an rgb tuple of int to a tkinter friendly color code"""
		if isinstance(rgb,str): return rgb
		r, g, b = rgb
		return f'#{r:02x}{g:02x}{b:02x}'

	def draw_pixel(self,col,row):
		x0 = self.MARGIN + col*self.PIXEL_SIZE + self.PIXEL_SIZE//2
		y0 = self.MARGIN + row*self.PIXEL_SIZE + self.PIXEL_SIZE//2
		x1 = x0 + self.PIXEL_SIZE
		y1 = y0 + self.PIXEL_SIZE
		color = self.board[col][row]
		self.canvas.create_rectangle(x0,y0,x1,y1,fill= self._from_rgb(color))

	def draw(self):
		for c in range(self.COLS):
			for r in range(self.ROWS):
				self.draw_pixel(c,r)

	def draw_remote(self,col,row):
		self.board[col][row] = self.container.color
		self.draw_pixel(col,row)			

	def click(self,event):
		if self.container.isDrawing :
			col = (event.x - (self.MARGIN + self.PIXEL_SIZE//2))//self.PIXEL_SIZE
			row = (event.y - (self.MARGIN + self.PIXEL_SIZE//2))//self.PIXEL_SIZE
			self.board[col][row] = self.container.color
			self.draw_pixel(col,row)
			print (f' Col: {col} , Row: {row}')
			self.container.sendMessage((col,row), 2)

	def clearBoard(self):
		if self.isDrawing :
			self.board = [[(0,255,255) for r in range(self.ROWS)] for c in range(self.COLS)]
			self.draw()
			self.canvas.update()
			self.canvas.update_idletasks()


