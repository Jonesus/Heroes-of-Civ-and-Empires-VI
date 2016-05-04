import pygame
from datetime import datetime
from menu import Button


# Color constants
BLACK = (  0,   0,   0)
GRAY  = ( 50,  50,  50)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
LGREEN= (100, 255, 100)
RED   = (255,   0,   0)
LRED  = (255, 100, 100)


# Visual constants
TASKBARHEIGHT = 152
TILESIZE = 32


# Movement constants
UP    = ( 0 , 1)
DOWN  = ( 0 ,-1)
LEFT  = ( 1 , 0)
RIGHT = (-1 , 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)



class Text:
    
    def __init__(self, text, x, y, size, screen, color = BLACK, font = None):
        
        self.x = x
        self.y = y
        self.screen = screen
        
        self.color = color
        self.font = pygame.font.SysFont(font, size)
        
        self.text = self.font.render(text, True, color)

    def draw(self):
        
        self.screen.blit(self.text, (self.x, self.y))

    
    def updateText(self, text):
        
        self.text = self.font.render(text, True, self.color)
        
    



class Taskbar:
    
    def __init__(self, screen, game):
        
        self.game = game
        self.screen = screen
        
        self.fontSpacing = (TASKBARHEIGHT - 30) // 5
        self.fontSize = self.fontSpacing - 5
        
        self.x = 0
        self.y = self.screen.get_height() - TASKBARHEIGHT
        self.width = self.screen.get_width()
        self.height = TASKBARHEIGHT
        
        
        self.imageSize = TASKBARHEIGHT // 2
        
        self.unitName  = Text("None", TASKBARHEIGHT, self.screen.get_height() - TASKBARHEIGHT + self.fontSpacing*1, self.fontSize, self.screen, WHITE)
        self.unitHP    = Text("None", TASKBARHEIGHT, self.screen.get_height() - TASKBARHEIGHT + self.fontSpacing*2, self.fontSize, self.screen, WHITE)
        self.unitDMG   = Text("None", TASKBARHEIGHT, self.screen.get_height() - TASKBARHEIGHT + self.fontSpacing*3, self.fontSize, self.screen, WHITE)
        self.unitRange = Text("None", TASKBARHEIGHT, self.screen.get_height() - TASKBARHEIGHT + self.fontSpacing*4, self.fontSize, self.screen, WHITE)
        self.unitMoves = Text("None", TASKBARHEIGHT, self.screen.get_height() - TASKBARHEIGHT + self.fontSpacing*5, self.fontSize, self.screen, WHITE)
        
        self.texts = [self.unitName, self.unitHP, self.unitDMG, self.unitRange, self.unitMoves]
    
    
    
    def updateTexts(self):
           
        if not self.game.selectedTile:
            return
        
        if not self.game.selectedTile.unit:
            return   
        
         
        self.unitName.updateText(self.game.selectedTile.unit.name) 
        self.unitHP.updateText("HP: " + str(self.game.selectedTile.unit.hp))
        self.unitDMG.updateText("DMG: " + str(self.game.selectedTile.unit.dmg))
        self.unitRange.updateText("Range: " + str(self.game.selectedTile.unit.range))
        self.unitMoves.updateText("Moves: " + str(self.game.selectedTile.unit.moves))
        
        
        
    def drawInfo(self):
        
        if not self.game.selectedTile:
            return
        
        if not self.game.selectedTile.unit:
            return
        
        img = pygame.transform.scale( self.game.selectedTile.unit.img, (self.imageSize,self.imageSize))

        self.screen.blit(img, ((TASKBARHEIGHT//4), self.screen.get_height() - (TASKBARHEIGHT//4 * 3)))
        
        for text in self.texts:
            text.draw()


    def draw(self):
        
        pygame.draw.rect(self.screen, BLACK, (self.x,self.y,self.width,self.height))
        self.drawInfo()





class Gameview:
    
    def __init__(self, screen, game):
        
        self.screen = screen
        self.game = game
        
        self.taskbar = Taskbar(self.screen, self.game)
        self.turnButton = Button("Next turn",self.screen.get_width() - 250, self.screen.get_height() - (TASKBARHEIGHT//2) - 25, 200, 50, GREEN, LGREEN, self.screen, action = self.game.switchTurn)
        
        self.viewx = int( self.screen.get_width() / TILESIZE )
        self.viewy = int( ( self.screen.get_height() - TASKBARHEIGHT ) / TILESIZE )
        
        
        self.mapx = self.game.xsize
        self.mapy = self.game.ysize
        
        self.currentx = 0
        self.currenty = 0
        
        
        
    def draw(self):
        
        ret = 0
        
        self.screen.fill(BLACK)
        self.taskbar.draw()
        
        if self.game.activePlayer.ID == 1:
            if self.game.activePlayer.actionsLeft():
                self.turnButton.color = GRAY
            else:
                self.turnButton.color = GREEN
            ret = self.turnButton.draw()
        
        
        for i in range(self.viewy):
            for j in range(self.viewx):
                
                self.screen.blit(pygame.transform.scale( self.game.map[i+self.currenty][j+self.currentx].img, (TILESIZE,TILESIZE)), \
                                 (j * TILESIZE, i * TILESIZE))
                
                if self.game.map[i+self.currenty][j+self.currentx].unit:
                    
                    self.screen.blit(self.game.map[i+self.currenty][j+self.currentx].unit.sprite, \
                                 (j * TILESIZE, i * TILESIZE))
                
                if self.game.selectedTile:
                    if self.game.selectedTile.x == j+self.currentx and \
                       self.game.selectedTile.y == i+self.currenty:
                        pygame.draw.rect(self.screen, (255,255,255), (j*TILESIZE, i*TILESIZE, TILESIZE,TILESIZE), 2)
                
                
                
                
                
                click = 1
                click, temp = self.game.map[i+self.currenty][j+self.currentx].click(self.screen, self.currentx, self.currenty, TILESIZE)
                if click == 1 and temp != None:
                    self.game.selectedTile = temp
                    self.taskbar.updateTexts()
                    
                    print("Tile at ({}, {})".format(self.game.selectedTile.x, self.game.selectedTile.y))
                    print("Pathable:", self.game.selectedTile.pathable)
                    if self.game.selectedTile.unit:
                        print("Has unit:", self.game.selectedTile.unit.name)
                        print("Moves left:", self.game.selectedTile.unit.moves)
                    print()
                
                
                elif click == 2 and temp != None:
                    if temp.unit:
                        self.game.dealDamage(self.game.selectedTile, temp)
                    else:
                        timenow = datetime.now()
                        self.game.moveUnit(self.game.selectedTile, temp)
                        print("Time elapsed:", datetime.now() - timenow, "\n")
                        
                    self.taskbar.updateTexts()
                    
        
        
        return 1          
        
    
    def moveView(self, direction):
        
        if (direction not in DIRECTIONS):
            return 0
        
        
        if (direction[0] + self.currentx) < 0 or \
            (direction[0] + self.currentx + self.viewx) > self.mapx:
            return 0
        
        if (direction[1] + self.currenty) < 0 or \
            (direction[1] + self.currenty + self.viewy) > self.mapy:
            return 0
 
           
        self.currentx += direction[0]
        self.currenty += direction[1]
        
        return 1






class Pauseview:
    
    def __init__(self, screen, game):
        
        self.screen = screen
        self.game = game












