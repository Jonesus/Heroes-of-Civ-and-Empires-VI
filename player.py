import pygame

class Player:
    
    def __init__(self, ID, startTile, game):
        
        
        self.ID = ID
        self.units = []
        self.startTile = startTile
        self.game = game
    
    
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
