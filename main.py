import pygame
from pygame.locals import *


from menu import Menu
from ui import UI
from game import Game

UP    = ( 0 ,-1)
DOWN  = ( 0 , 1)
LEFT  = (-1 , 0)
RIGHT = ( 1 , 0)


def main():
    
    pygame.display.init()
    pygame.init()
    
    displayWidth = 800
    displayHeight = 600
    screenSize = (displayWidth, displayHeight)
    
    gameScreen = pygame.display.set_mode(screenSize)
    gameClock = pygame.time.Clock()
    pygame.display.set_caption("Heroes of Civ and Empires VI")
    FPS = 30
    
    game = Game("maps/default.txt")
    
    
    mainMenu = Menu(gameScreen)
    gameUI = UI(gameScreen, game)
    
    activeDisplay = 0
    
    displays = [mainMenu, gameUI]
    
    
    
    running = True
    
    while running:
        
        activeDisplay = displays[activeDisplay].draw()
        
        pygame.display.update()
        gameClock.tick(FPS)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    activeDisplay = 0

                elif event.key == K_UP and activeDisplay == 1:
                    gameUI.gameview.moveView(UP)
                    
                elif event.key == K_DOWN and activeDisplay == 1:
                    gameUI.gameview.moveView(DOWN)
                    
                elif event.key == K_LEFT and activeDisplay == 1:
                    gameUI.gameview.moveView(LEFT)

                elif event.key == K_RIGHT and activeDisplay == 1:
                    gameUI.gameview.moveView(RIGHT)









main()


