import tkinter as tk
from tkinter import ttk
import threading

class MainMenu(tk.Toplevel):
	def __init__(self, container):
		super().__init__(container)
		self.container = container
		self.title("Login")
		self.resizable(width=False,height=False)
		self.configure(width=400,height=300)
		# create a Label
		self.pls = ttk.Label(self,
						text="Please login to continue",
						justify=tk.CENTER,
						font="Helvetica 14 bold")

		self.pls.place(relheight=0.15,relx=0.2,rely=0.07)
		# create a Label
		self.labelName = ttk.Label(self,text="Name: ",font="Helvetica 12")
		self.labelName.place(relheight=0.2,relx=0.1,rely=0.2)

		# create a entry box for
		# tyoing the message
		self.entryName = ttk.Entry(self,font="Helvetica 14")
		self.entryName.place(relwidth=0.4,relheight=0.12,relx=0.35,rely=0.2)

		# set the focus of the cursor
		self.entryName.focus()

		# create a Continue Button
		# along with action
		self.go = ttk.Button(self,
						text="CONTINUE",
						# font="Helvetica 14 bold",
						command=lambda: self.goAhead(self.entryName.get()))

		self.bind ('<Return>', self.returnPressed)

		self.go.place(relx=0.4,rely=0.55)
		# self.container.mainloop()

	def returnPressed(self,event):
		if self.entryName.get():
			self.goAhead(self.entryName.get())	

	def goAhead(self, name):
		self.container.deiconify()
		self.destroy()

		self.container.name = name

		# the thread to receive messages
		self.container.connectServer()
		rcv = threading.Thread(target=self.container.receive)
		rcv.start()

	