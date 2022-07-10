class Player():
	def __init__(self,conn, name,id) -> None:
		self.conn = conn
		self.name = name
		self.id = id
		self.gameID = 0
		self.isDrawing = False
		self.score = 0


