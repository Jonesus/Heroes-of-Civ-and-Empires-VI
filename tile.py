import pygame


LANDSCAPES = {"M":(False, "tiles/mountain.png"), \
              "G":(True, "tiles/grass.png"), \
              "W":(False, "tiles/water.png")}



class Tile:
    
    def __init__(self, x, y, landscape):
        
        self.x = x
        self.y = y
        
        self.unit = None
        
        self.pathable = LANDSCAPES[landscape][0]
        self.img      = pygame.image.load( LANDSCAPES[landscape][1] ).convert()
        
        
    def addUnit(self, unit):
        if self.unit:
            return 0
        
        self.unit = unit
        return 1
    
    
    
    