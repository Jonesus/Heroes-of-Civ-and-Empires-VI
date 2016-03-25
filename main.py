import pygame




BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)


def main():
    
    pygame.display.init()
    
    displayWidth = 800
    displayHeight = 600
    screenSize = (displayWidth, displayHeight)
    
    gameScreen = pygame.display.set_mode(screenSize)
    gameClock = pygame.time.Clock()
    pygame.display.set_caption("Heroes of Civ and Empires VI")
    FPS = 30
    
    defaultFont = pygame.font.SysFont(None, 20)
    
    
    
    def button(text, x, y, width, height, color, activeColor, action = None):
        mousePos = pygame.mouse.get_pos()
        clicked = pygame.mouse.get_pressed()
        
        if x+width > mousePos[0] > x and y+height > mousePos[1] > y:
            pygame.draw.rect(gameScreen, activeColor,(x,y,width,height))
            if clicked[0] == 1 and action != None:
                action()
            
        else:
            pygame.draw.rect(gameScreen, color,(x,y,width,height))

        text = defaultFont.render(text, True, BLACK)
        textRect = text.get_rect()
        
        textRect.center = ( (x+(width/2)), (y+(height/2)) )
        gameScreen.blit(text, textRect)





