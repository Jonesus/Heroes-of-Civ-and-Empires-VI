UP    = ( 1 , 0)
DOWN  = (-1 , 0)
LEFT  = ( 0 ,-1)
RIGHT = ( 0 , 1)

DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

# X and Y coordinate additions for movement in each direction

class Unit:
    
    def __init__(self, x, y, sourcefile):
        
        file = open(sourcefile, 'r')
        self.attributedict = {}
        
        for line in file:
            linelist = line.split(':')
            attributedict[ linelist[0] ] = linelist[1]
        
        file.close()
        
        self.x = x
        self.y = y
        self.name = attributedict["NAME"]
        self.hp = attributedict["HP"]
        self.dmg = attributedict["DMG"]
        self.range = attributedict["RANGE"]
        self.moves = attributedict["MOVES"]
        

        
    def move(self, direction):
        
        if direction not in DIRECTIONS or self.moves == 0:
            return 0
        
        self.x += direction[0]
        self.y += direction[1]
        
        self.moves -= 1
        
        return 1
    
    
    
    def resetMoves(self):
        self.moves = self.attributedict["MOVES"]
    
    
    
    
    
    
        
        
        