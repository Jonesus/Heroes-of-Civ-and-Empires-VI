from tile import Tile


class Game:
    
    def __init__(self, mapfile):
        
        
        self.map, self.xsize, self.ysize = self.generateMap(mapfile)
        
        self.activeplayer = None
        self.inactiveplayer = None
        
    
    
    
        
    def generateMap(self, mapfile):
        
        gamemap = []
        
        file = open(mapfile, 'r')
        
        i = j = 0
        for line in file:
            gamemap.append([])
            line = line.rstrip()
            for char in line:
                gamemap[i].append( Tile(j, i, char) )
                j += 1
            xsize = j
            j = 0
            i += 1
        ysize = i
        
        return gamemap, xsize, ysize
    
    
    
    def processTurn(self, player):
        pass
        
    
    
    
    
    
    
    
    
    