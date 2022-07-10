import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
import threading


class Chat(ttk.Frame):
	def __init__(self,container):
		ttk.Frame.__init__(self,container)
		self.container = container
		self.grid(column=2, row=1, rowspan=2)
		
		self.labelTop = ttk.Label(self,text = "Chat Room: ")
		self.labelTop.pack(fill=tk.BOTH)

		self.textChat = ScrolledText(self, width = 50, height = 40)
		self.textChat.pack(fill=tk.BOTH, side = tk.TOP, expand = True)

		# self.labelBottom = ttk.Label(self)
		# self.labelBottom.pack(fill=tk.BOTH)

		self.entryMsg = ttk.Entry(self)

		self.entryMsg.pack(fill=tk.BOTH, side = tk.TOP)

		self.entryMsg.focus()

		self.buttonMsg = ttk.Button(self,
                                text="Send",
                                command=lambda: self.sendButton(self.entryMsg.get()))

		self.buttonMsg.pack(side = tk.TOP)



	def addText(self,txt,user = None):
		self.textChat.insert(tk.END, f'Player: {user} - {txt}')

	def sendButton(self, txt):
		txt = f'{self.container.name}: {txt}'
		print (f'sending" {txt}')
		self.textChat.config(state=tk.DISABLED)
		self.msg = txt
		self.entryMsg.delete(0, tk.END)
		snd = threading.Thread(target=self.container.sendMessage, args=(txt,0))
		snd.start()




