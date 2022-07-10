import tkinter as tk
from tkinter import ttk

class TopPanel(ttk.Frame):
	def __init__(self,container):
		ttk.Frame.__init__(self,master = container)
		s = ttk.Style()
		s.configure('Frame2.TFrame', background='green')
		self.configure(style='Frame2.TFrame')
		self.container = container
		self.padding = 50
		self.MARGIN = 20
		# self.WIDTH = 40

		# self['width'] = 00
		# self['height'] = 30
		
		self.grid(column=0, row=0, columnspan=3,sticky=tk.W+tk.E, padx = 10, pady = 10)
		
		
		self.canvas = tk.Canvas(self,height = 50, bg = 'yellow')
		self.canvas.pack(fill=tk.BOTH, side = tk.TOP, expand = True, padx = 10, pady = 10)
		self.canvas.update()
		# self.frameWidth = self.canvas.winfo_reqwidth()
		# print (f'TopPanel width: {self.canvas.winfo_width()}, reqwidth: {self.canvas.winfo_reqwidth()}, width : {self.frameWidth}')
		self.draw()

	def draw (self):
		# for i in range(15):
		# 	self.canvas.create_text(i*100, self.MARGIN, text=f'{i}' , fill="black", font=('Helvetica 15 bold'))
		if self.container.inGame:
			roundTxt = f"Round {self.container.roundID} / {len(self.container.players)}"
			
			self.canvas.create_text(150, self.MARGIN, text=roundTxt , fill="black", font=('Helvetica 15 bold'))
			self.canvas.create_text(650, self.MARGIN, text=self.container.word , fill="black", font=('Helvetica 15 bold'))

		if self.container.gameOver:
			self.canvas.delete("all")
			self.canvas.create_text(650, self.MARGIN, text="Game Over" , fill="black", font=('Helvetica 15 bold'))

	def drawTimer(self, time):
		if not self.container.gameOver:
			self.canvas.delete("all")
			self.draw()
			self.canvas.create_text(1300, self.MARGIN, text=time , fill="black", font=('Helvetica 15 bold'))