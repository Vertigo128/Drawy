import time
import threading

class Round():
	def __init__(self, id, word, game) -> None:
		self.id = id
		self.game = game
		self.time = 0
		self.word = word
		self.setPlayers()
		timer = threading.Thread(target=self.timer, args = (30,))
		timer.start()
		
	
	def setPlayers(self):
		
		for player in self.game.playerList:
			print (f'check if {player.name} is drawing: {player.isDrawing}')
			if player.isDrawing: 
				print (f'player {player.name} is drawing_0' )
				self.game.n.broadcastMessage(f'player {player.name} is drawing', msgType = 0)
				print (f'player {player.name} is drawing_1' )
				self.game.n.sendMessage(player.conn, True , msgType = 1)
			else:
				self.game.n.sendMessage(player.conn, False , msgType = 1)

	
	

	
	def timer (self, timeLimit = 30):
		currentRound = self.game.roundID
		for i in range(timeLimit):
			self.time = i
			time.sleep (1)
			if i%10 == 0 : self.game.n.broadcastMessage(f'{timeLimit - i}', msgType = 7)

		if self.game.roundID == currentRound:
			self.game.n.broadcastMessage(f'Times up', 0)
			self.game.endRound()
	

	def guess(self,player, word):
		if word==self.word and not player.isDrawing:
			self.game.n.broadcastMessage(f'{player.name} guess correctly', 0)
			player.score  += (30 - self.time)
			self.game.endRound()



