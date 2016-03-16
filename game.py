from tile import Tile


class Game:
    
    def __init__(self, mapfile):
        
        
        self.map = self.generateMap(mapfile)
        
        self.activeplayer = None
        self.inactiveplayer = None
        
    
    
    
        
    def generateMap(self, mapfile):
        
        gamemap = []
        
        file = open(mapfile, 'r')
        
        i = j = 0
        for line in file:
            line = line.rstrip()
            for char in line:
                gamemap[i].append( Tile(j, i, char) )
                j += 1
            j = 0
            i += 1
        
        
        return gamemap
    
    
    
    def processTurn(self, player):
        
        
    
    
    
    
    
    
    
    
    