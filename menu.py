import pygame

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
LGREEN= (100, 255, 100)
RED =   (255,   0,   0)
LRED =  (255, 100, 100)


class Button:
    
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
                self.action()
            
        else:
            pygame.draw.rect(self.screen, self.color,(self.x,self.y,self.width,self.height))

        self.screen.blit(self.text, self.textRect)



class Text:
    
    def __init__(self, text, x, y, size, screen, color = BLACK, font = None):
        
        self.x = x
        self.y = y
        self.screen = screen

        self.font = pygame.font.SysFont(font, size)
        self.text = self.font.render(text, True, color)

    def draw(self):
        
        self.screen.blit(self.text, (self.x - self.text.get_width()/2, self.y))
    
    
    
class Menu:
    
    def __init__(self, screen):
        
        self.screen = screen
        
        self.startButton = Button("Start",self.screen.get_width()/2-100, self.screen.get_height()/2-50, 200, 50, GREEN, LGREEN, self.screen)
        self.quitButton = Button("Quit",self.screen.get_width()/2-100, self.screen.get_height()/2+50, 200, 50, RED, LRED, self.screen, action = quit)
        
        self.titleText = Text("Heroes of Civ and Empires VI", self.screen.get_width()/2, self.screen.get_height()/2-200, 40, self.screen, font = "Comic Sans MS")
        
        self.objects = [self.startButton, self.quitButton, self.titleText]
        


    def draw(self):
        
        self.screen.fill(WHITE)
        for thing in self.objects:
            thing.draw()









