from player import Player
from round import Round
from random import choice


class Game():
	def __init__(self, id, playerList, network) -> None:
		self.playerList = playerList
		self.nPlayers = len(playerList)
		self.gameID = id
		self.playerDrawing = 0
		self.gameOn = True
		self.roundID = 1
		self.round = None
		self.n = network
		self.words = open("./server/words.txt", 'r').readlines()

		self.startRound()
	
	def startRound(self):
		
		self.n.broadcastMessage(f'Starting Round {self.roundID} out of {self.nPlayers}', 0)
		self.n.broadcastMessage(self.getLeaderboards(), 4)
		self.n.broadcastMessage(self.roundID, 6)
		word = self.getWord()
		for c,player in enumerate (self.playerList):
			player.isDrawing = True if c==self.playerDrawing else False
			userWord = word if player.isDrawing else "_ "*len(word)
			self.n.sendMessage(player.conn, userWord, 8)
		self.playerList[self.playerDrawing].isDrawing = True
		self.round = Round(self.roundID, word, self)
		self.playerDrawing +=1

	def getPlayerFromMessage (self, msg : str):
		name = msg[:msg.find(":")]
		for player in self.playerList:
			if player.name == name:
				return player

	def getWord(self):
		word = choice(self.words)
		self.words.remove(word)
		return word.strip()

	def endRound(self):
		self.roundID +=1
		self.n.broadcastMessage(self.getLeaderboards(), 4)
		if self.roundID >= self.nPlayers + 1 :
			self.n.broadcastMessage(f'Game Over', 9)

		else : 
			self.startRound()

	def getLeaderboards(self):
		leaders = dict()
		for player in self.playerList:
			leaders[player.name] = player.score
		return leaders










