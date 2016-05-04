import pygame



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
    
    
    def __init__(self, playerid, sourcefile):
        
        self.attributedict = {}
        with open(sourcefile, 'r') as file:
            for line in file:
                linelist = line.split(':')
                self.attributedict[ linelist[0] ] = linelist[1].rstrip()
        
        self.playerID = playerid
        self.name  =      self.attributedict["NAME"]
        self.hp    = int( self.attributedict["HP"]    )
        self.dmg   = int( self.attributedict["DMG"]   )
        self.range = int( self.attributedict["RANGE"] )
        self.moves = int( self.attributedict["MOVES"] )
        
        self.tag = None
        
        self.img = pygame.image.load( self.attributedict["IMG"] ).convert_alpha()
        self.sprite = pygame.image.load( self.attributedict["SPRITE"] ).convert_alpha()

        

    
    def resetMoves(self):
        self.moves = int( self.attributedict["MOVES"] )
    
    
    
    
    
    
        
        
        