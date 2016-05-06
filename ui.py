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


# Movement constants
UP    = ( 0 , 1)
DOWN  = ( 0 ,-1)
LEFT  = ( 1 , 0)
RIGHT = (-1 , 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)









class Text:
    
    '''
    Represents a generic piece of text shown on screen.
    
    Params:
    text: Text in button
    x, y: Coordinates for top left of button
    size: Font size
    screen: pygame screen where button is drawn
    color: Color of text
    font: font of text
    
    Methods:
    draw(): Draws the text on the screen
    '''
    
    
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
    
    '''
    Represents the taskbar of the game view.
    
    Params:
    screen: pygame screen
    game: instance of Game class
    
    Methods:
    updateTexts: Updates the unit attribute texts shown on the taskbar
    drawInfo: Draws the unit attribute tetxs
    draw: Draws the whole taskbar
    '''
    
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
    
    '''
    Represents the game as shown to the player.
    
    Params:
    screen: Pygame screen
    game: Instance of Game class
    gameover: Gameover popup window
    tilesize: Size of each tile read from setup.txt
    
    Methods:
    draw(): Draws the view
    moveView(): Moves the current viewpoint
    
    '''
    
    
    def __init__(self, screen, game, gameover, tilesize):
        
        self.TILESIZE = tilesize
        
        self.gameover = gameover
        self.screen = screen
        self.game = game
        
        self.taskbar = Taskbar(self.screen, self.game)
        self.turnButton = Button("Next turn",self.screen.get_width() - 250, self.screen.get_height() - (TASKBARHEIGHT//2) - 25, 200, 50, GREEN, LGREEN, self.screen, action = self.game.switchTurn)
        
        
        # Maximum values for drawing tiles as limited by window resolution
        reslimitx = int( self.screen.get_width() / self.TILESIZE )
        reslimity = int( ( self.screen.get_height() - TASKBARHEIGHT ) / self.TILESIZE )
        
        self.viewx = reslimitx if reslimitx < self.game.xsize else self.game.xsize
        self.viewy = reslimity if reslimity < self.game.ysize else self.game.ysize
        
        # Map dimensions
        self.mapx = self.game.xsize
        self.mapy = self.game.ysize
        
        # Offset from top left corner for drawing current view
        self.currentx = 0
        self.currenty = 0
        
        
        
    def draw(self):
        
        
        self.screen.fill(BLACK)
        self.taskbar.draw()
        
        
        # Draw the "next turn" button
        
        if self.game.activePlayer.ID == 1:
            if self.game.activePlayer.actionsLeft():
                self.turnButton.color = GRAY
            else:
                self.turnButton.color = GREEN
            self.turnButton.draw()
        
        # Draw the tiles and units
        
        for i in range(self.viewy):
            for j in range(self.viewx):
                
                self.screen.blit(pygame.transform.scale( self.game.map[i+self.currenty][j+self.currentx].img, (self.TILESIZE,self.TILESIZE)), \
                                 (j * self.TILESIZE, i * self.TILESIZE))
                
                if self.game.map[i+self.currenty][j+self.currentx].unit:
                    
                    self.screen.blit(pygame.transform.scale( self.game.map[i+self.currenty][j+self.currentx].unit.sprite, (self.TILESIZE,self.TILESIZE)),\
                                 (j * self.TILESIZE, i * self.TILESIZE))
                
                if self.game.selectedTile:
                    if self.game.selectedTile.x == j+self.currentx and \
                       self.game.selectedTile.y == i+self.currenty:
                        pygame.draw.rect(self.screen, (255,255,255), (j*self.TILESIZE, i*self.TILESIZE, self.TILESIZE,self.TILESIZE), 2)
                
                
                
                # Process player clicks on the map tiles
                
                click = 1
                click, temp = self.game.map[i+self.currenty][j+self.currentx].click(self.screen, self.currentx, self.currenty, self.TILESIZE)
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
                        self.game.moveUnit(self.game.selectedTile, temp)
                        
                    self.taskbar.updateTexts()
                    
        
        # Check for game over
        
        if not self.game.player1.unitsLeft() and not self.game.gameover:
            self.gameover.winnerText.updateText("You lose!")
            self.game.gameover = True
            return 3
        
        if not self.game.player2.unitsLeft():
            self.gameover.winnerText.updateText("You win!")
            self.game.gameover = True
            return 3
        
        
        
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












class Popup:
    
    '''
    Represents a generic popup window
    '''
    
    def __init__(self, screen, game):
        
        self.screen = screen
        self.game = game
        
        self.x = 100
        self.y = 100
        self.height = self.screen.get_height() - 200
        self.width = self.screen.get_width() - 200
        
        self.objects = []


    def draw(self):
        
        pygame.draw.rect(self.screen, WHITE, (self.x-5,self.y-5,self.width+10,self.height+10))
        pygame.draw.rect(self.screen, BLACK, (self.x,self.y,self.width,self.height))
        
        for thing in self.objects:
            ret = thing.draw()
            if ret != None:
                return ret
    
    
    
    




class Pauseview(Popup):
    
    '''
    Represents the popup shown when player pauses the game
    '''
    
    def __init__(self, screen, game):
        
        Popup.__init__(self, screen, game)
        
        self.pausedText = Text("Game paused", self.screen.get_width()/2, self.y+40, 30, self.screen, BLUE,"Comic Sans MS")
        self.continueButton = Button("Continue",self.screen.get_width()/2-100, self.height/2+50, 200, 50, GREEN, LGREEN, self.screen, action = self.continueGame)
        self.endButton      = Button("End game",self.screen.get_width()/2-100, self.height/2+150, 200, 50, RED,   LRED,   self.screen, action = self.endGame)
        
        self.pausedText.x = self.pausedText.x - self.pausedText.text.get_width()/2
        
        self.objects = [self.pausedText, self.continueButton, self.endButton]


    def continueGame(self):
        return 1
    
    
    def endGame(self):
        return 0









class Gameover(Popup):

    '''
    Represents the popup shown when the game is over
    '''
    
    def __init__(self, screen, game):
        
        Popup.__init__(self, screen, game)
        
        self.winnerText = Text("You win!", self.screen.get_width()/2, self.y+40, 30, self.screen, BLUE,"Comic Sans MS")
        self.continueButton = Button("Continue",self.screen.get_width()/2-100, self.height/2+50, 200, 50, GREEN, LGREEN, self.screen, action = self.continueGame)
        self.endButton      = Button("Go to menu",self.screen.get_width()/2-100, self.height/2+150, 200, 50, RED,   LRED,   self.screen, action = self.gotoMenu)
        
        self.winnerText.x = self.winnerText.x - self.winnerText.text.get_width()/2
        
        self.objects = [self.winnerText, self.continueButton, self.endButton]


    def continueGame(self):
        return 1
    
    
    def gotoMenu(self):
        return 0




