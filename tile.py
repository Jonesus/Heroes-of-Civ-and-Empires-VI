import pygame
import time

'''
LANDSCAPES = {".":(True,  "graphics/tiles/grass.png"),    \
              ",":(True,  "graphics/tiles/grass.png"),    \
              "G":(True,  "graphics/tiles/grass.png"),    \
              "M":(False, "graphics/tiles/mountain.png"), \
              "W":(False, "graphics/tiles/water.png")}


'''

class Tile:
    
    '''
    Represents a single tile or square in the game map.
    
    Params:
    x: x-coordinate of tile
    y: y-coordinate of tile
    landscape: type of terrain
    
    Attributes:
    unit: unit currently in tile if any
    visited: used in pathfinding algorithm to check if tile has been visited in search
    previous: used in pathfinding algorithm to store previous tile in found path
    pathable: can a unit walk through the tile
    img: image of landscape shown on playing field
    
    Methods:
    addUnit(): add unit to tile and make it unpathable
    click(): checks if tile has been clicked by player
    '''
    
    def __init__(self, x, y, landscape, mapsyntax):
        
        self.x = x
        self.y = y
        
        LANDSCAPES = {}
        
        try:
            for line in mapsyntax:
                if line[1][1] != "True" and line[1][1] != "False":
                    raise IndexError
                pathable = True if line[1][1] == "True" else False
                LANDSCAPES[line[0]] = (pathable, line[1][0])
        
        except IndexError:
            print("Illegal map syntax!")
            with open("log.txt", "w") as out:
                out.write("Illegal map syntax!")
            quit()
            
        
        self.startpos = None
        if landscape == ".":
            self.startpos = 1
        elif landscape == ",":
            self.startpos = 2
        
        
        self.unit     = None
        self.visited  = False
        self.previous = None
        
        try:
            self.pathable = LANDSCAPES[landscape][0]
            self.img      = pygame.image.load( LANDSCAPES[landscape][1] ).convert()
        except KeyError:
            print("Map keys not found!")
            with open("log.txt", "w") as out:
                out.write("Map keys not found!")
            quit()
        except pygame.error:
            print("Invalid tile image!")
            with open("log.txt", "w") as out:
                out.write("Invalid tile image!")
            quit()
    
        
    def addUnit(self, unit):
        self.pathable = False
        self.unit = unit
    
    
    
    def click(self, screen, currentx, currenty, size):
        
        mousePos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        
        if (self.x-currentx)*size+size > mousePos[0] >= (self.x-currentx)*size and (self.y-currenty)*size+size > mousePos[1] >= (self.y-currenty)*size:
            pygame.draw.rect(screen, (0,0,0), ((self.x-currentx)*size,(self.y-currenty)*size,size,size), 2)
            if clicked[0] == 1:
                time.sleep(0.1)
                pygame.event.poll()
                clicked = pygame.mouse.get_pressed()
                if clicked[0] == 0:
                    return 1, self
            elif clicked[2] == 1:
                time.sleep(0.1)
                pygame.event.poll()
                clicked = pygame.mouse.get_pressed()
                if clicked[2] == 0:
                    return 2, self
            
        return 0, None
    
        
    
    
    
    
    
    