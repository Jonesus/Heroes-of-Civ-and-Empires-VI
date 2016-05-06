import pygame



class Unit:
    
    '''
    Represents a unit in the game.
    
    Params:
    playerid: which player unit belongs to
    sourcefile: path to file to read unit's attributes from
    
    Attributes:
    playerID: which player unit belongs to
    name:  unit name/type
    hp:    hitpoints, the amount of damage the unit can survive
    range: range of unit's attacks measured in tiles
    moves: amount of actions unit can take in a turn
    tag: temporary variable for example group leader info
    img: image of unit shown on toolbar
    sprite: image of unit shown on playing field
    
    Methods:
    resetMoves():    resets the unit's moves to default amount given in file
    '''
    
    def __init__(self, playerid, sourcefile):
        
        
        try:
            self.attributedict = {}
            with open(sourcefile, 'r') as file:
                for line in file:
                    
                    if line[0] == "#" or line[0] == "\n":
                        continue
                    
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
        
        except ValueError:
            print("Illegal values in unit file!")
            with open("log.txt", "w") as out:
                out.write("Illegal values in unit file!")
            quit()
            
        except KeyError:
            print("Illegal keys in unit file!")
            with open("log.txt", "w") as out:
                out.write("Illegal keys in unit file!")
            quit()
            
        except pygame.error:
            print("Invalid unit image!")
            with open("log.txt", "w") as out:
                out.write("Invalid unit image!")
            quit()
        

    
    def resetMoves(self):
        self.moves = int( self.attributedict["MOVES"] )
    
    
    
    
    
    
        
        
        