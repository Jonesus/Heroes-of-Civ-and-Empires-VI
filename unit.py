UP    = ( 1 , 0)
DOWN  = (-1 , 0)
LEFT  = ( 0 ,-1)
RIGHT = ( 0 , 1)

DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

# X and Y coordinate additions for movement in each direction

class Unit:
    
    '''
    Represents a unit in the game.
    
    Params:
    x:     starting x-coordinate
    y:     starting y-coordinate
    sourcefile: path to file to read unit's attributes from
    
    Attributes:
    x:     x-coordinate
    y:     y-coordinate
    name:  unit name/type
    hp:    hitpoints, the amount of damage the unit can survive
    range: range of unit's attacks measured in tiles
    moves: amount of actions unit can take in a turn
    
    Methods:
    move(direction): moves the unit one tile in the direction given as parameter
    resetMoves():    resets the unit's moves to default amount given in file
    
    '''
    
    
    def __init__(self, x, y, sourcefile):
        
        file = open(sourcefile, 'r')
        self.attributedict = {}
        
        for line in file:
            linelist = line.split(':')
            self.attributedict[ linelist[0] ] = linelist[1]
        
        file.close()
        
        self.x = x
        self.y = y
        self.name = self.attributedict["NAME"]
        self.hp = self.attributedict["HP"]
        self.dmg = self.attributedict["DMG"]
        self.range = self.attributedict["RANGE"]
        self.moves = self.attributedict["MOVES"]
        

        
    def move(self, direction):
        
        if direction not in DIRECTIONS or self.moves == 0:
            return 0
        
        self.x += direction[0]
        self.y += direction[1]
        
        self.moves -= 1
        
        return 1
    
    
    
    def resetMoves(self):
        self.moves = self.attributedict["MOVES"]
    
    
    
    
    
    
        
        
        