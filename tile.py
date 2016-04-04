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
    
    
    
    def click(self, screen, currentx, currenty, size):
        
        mousePos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        
        if (self.x-currentx)*size+size > mousePos[0] >= (self.x-currentx)*size and (self.y-currenty)*size+size > mousePos[1] >= (self.y-currenty)*size:
            pygame.draw.rect(screen, (0,0,0), ((self.x-currentx)*size,(self.y-currenty)*size,size,size), 2)    
            if clicked[0] == 1:
                return self
            
        return None
    
        
    
    
    
    
    
    