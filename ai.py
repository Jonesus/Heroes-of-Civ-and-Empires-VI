from player import Player
from random import randint



class AI(Player):
    
    def __init__(self, ID, startTile, game):
        
        Player.__init__(self, ID, startTile, game)
        pass
    
    
    def evaluateMap(self):
        
        pass
    
    
    
    def createTask(self, unit):
        
        pass
    
    
    
    def averageDistance(self):
        
        
        
        def randDistance(iters):
            
            coordList = []
            pathList = []
            
            for i in range(iters):
                rand1 = randint(0, len(self.units))
                rand2 = randint(0, len(self.game.player1.units))
                
                x1 = self.units[rand1].x
                y1 = self.units[rand1].y
                
                x2 = self.game.player1.units[rand2].x
                y2 = self.game.player1.units[rand2].y
                
                coordList.append( ((x1,y1),(x2,y2)) )
            
            x1sum = x2sum = y1sum = y2sum = 0
            
            for i in range(iters):
                x1sum += coordList[i][0][0]
                y1sum += coordList[i][0][1]
                x2sum += coordList[i][1][0]
                y2sum += coordList[i][1][1]
                
            x1sum = x1sum // iters
            y1sum = y1sum // iters
            x2sum = x2sum // iters
            y2sum = y2sum // iters
            
            
            
            
            
            
            
            
            
            
        
        
        
        
        
