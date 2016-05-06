import pygame
import time

BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
BLUE   = (  0,   0, 255)
GREEN  = (  0, 255,   0)
LGREEN = (100, 255, 100)
RED    = (255,   0,   0)
LRED   = (255, 100, 100)


class Button:
    
    '''
    Represents a generic clickable button in menus or GUI
    
    Params:
    text: Text in button
    x, y: Coordinates for top left of button
    width, height: Dimensions
    color: Color of button when not hovering over it
    activeColor: Color of button when hovering over it
    screen: pygame screen where button is drawn
    font: Font for button text
    action: Function to execute when button is clicked
    
    Methods:
    draw(): Draws the button and checks if it is being hovered over
            or if it's clicked
    
    '''
    
    
    def __init__(self, text, x, y, width, height, color, activeColor, \
                 screen, font = None, action = None):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.activeColor = activeColor
        self.screen = screen
        self.action = action
        
        
        self.font = pygame.font.SysFont(font, 20)
        
        self.text = self.font.render(text, True, BLACK)
        self.textRect = self.text.get_rect()
        self.textRect.center = ( (x+(width/2)), (y+(height/2)) )
            
            
    def draw(self):
        
        mousePos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        
        if self.x+self.width > mousePos[0] > self.x and self.y+self.height > mousePos[1] > self.y:
            pygame.draw.rect(self.screen, self.activeColor,(self.x,self.y,self.width,self.height))
            if clicked[0] == 1 and self.action != None:
                time.sleep(0.1)
                pygame.event.poll()
                clicked = pygame.mouse.get_pressed()
                if clicked[0] == 0:
                    return self.action()
            
        else:
            pygame.draw.rect(self.screen, self.color,(self.x,self.y,self.width,self.height))

        self.screen.blit(self.text, self.textRect)
        return None


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

        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, color)

    def draw(self):
        
        self.screen.blit(self.text, (self.x - self.text.get_width()/2, self.y))
    
    
    
class Menu:
    
    '''
    Represents the main menu of the game
    '''
    
    
    def __init__(self, screen, game, gameparams):
        
        self.gameparams = gameparams
        self.game = game
        self.screen = screen
        
        self.startButton = Button("Start",self.screen.get_width()/2-100, self.screen.get_height()/2-50, 200, 50, GREEN, LGREEN, self.screen, action = self.startGame)
        self.quitButton = Button("Quit",self.screen.get_width()/2-100, self.screen.get_height()/2+50, 200, 50, RED, LRED, self.screen, action = self.quitGame)
        
        self.titleText = Text("Heroes of Civ and Empires VI", self.screen.get_width()/2, self.screen.get_height()/2-200, 40, self.screen, BLUE,"Comic Sans MS")
        
        self.objects = [self.startButton, self.quitButton, self.titleText]
        


    def draw(self):
        
        self.screen.fill(WHITE)
        for thing in self.objects:
            ret = thing.draw()
            if ret != None:
                return 1
        
        return None

    
    
    def startGame(self):
        self.game.__init__(self.gameparams[0], self.gameparams[1], self.gameparams[2], self.gameparams[3])
        return 1

    
    def quitGame(self):
        quit()




