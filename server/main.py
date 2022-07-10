# import socket library
import socket
import pickle
# import threading library
import threading
from player import Player
from game import Game
from network import Network




class Main():
    def __init__(self) -> None:
        self.gameID = 0
        self.playerID = 0
        self.clients, self.names = [], []
        self.playerList = []
        self.nPlayers = 2
        self.n = Network(self)
        self.n.startChat()

        
 
    def handleQueue(self):
        self.n.broadcastMessage([player.name for player in self.playerList],msgType=5)
        if len(self.playerList)>=self.nPlayers:
            self.n.broadcastMessage(f"Game Started",msgType=0)
            self.n.broadcastMessage(f"Game Started",msgType=-2)
            
            game = Game (self.gameID,self.playerList, self.n)
            self.n.game = game
            for player in self.playerList:
                player.gameID = self.gameID
            
            self.gameID += 1
            
        else:
            self.n.broadcastMessage(f"{len(self.playerList)} out of {self.nPlayers} players have joined the game",msgType=0)
            


 
       


# call the method to
# begin the communication
if __name__ == '__main__':
    main = Main()
