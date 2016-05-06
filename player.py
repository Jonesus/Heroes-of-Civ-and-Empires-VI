import pygame

class Player:
    
    def __init__(self, ID, startTile, game):
        
        '''
        Represents a player of the game.
        
        Params:
        ID: player ID
        startTile: player's start position tile
        game: current game instance
        
        Attributes:
        units: list of player's units
        
        Methods:
        actionsLeft(): returns whether player's units have left
        colorizeUnits(): recolors player's units
        resetUnits(): resets player's units moves
        
        '''
        
        
        self.ID = ID
        self.units = []
        self.startTile = startTile
        self.game = game
    
    
    def unitsLeft(self):
        
        if len(self.units) > 0:
            return True
        return False
    
    
    
    def actionsLeft(self):
        
        for unit in self.units:
            if unit.moves > 0:
                return True
        
        return False
    
    def colorizeUnits(self, colour):
        
        for unit in self.units:
            arr = pygame.PixelArray(unit.sprite)
            arr.replace((255,255,255), colour)
            del arr
    
    
    def resetUnits(self):
        
        for unit in self.units:
            unit.resetMoves()
