import pygame
from pygame.locals import *


from menu import Menu
from ui import Gameview, Pauseview
from game import Game

UP    = ( 0 ,-1)
DOWN  = ( 0 , 1)
LEFT  = (-1 , 0)
RIGHT = ( 1 , 0)


def main():
    
    # Initialize all pygame constants and variables
    
    pygame.display.init()
    pygame.init()
    
    displayWidth = 800
    displayHeight = 600
    screenSize = (displayWidth, displayHeight)
    
    gameScreen = pygame.display.set_mode(screenSize)
    gameClock = pygame.time.Clock()
    pygame.display.set_caption("Heroes of Civ and Empires VI")
    FPS = 30
    
    # Initialize the game itself, read default file for map
    
    game = Game("maps/default.txt")
    
    # Initialize 
    
    mainMenu = Menu(gameScreen, game)
    gameUI = Gameview(gameScreen, game)
    
    paused = Pauseview(gameScreen, game)
    
    activeDisplay = 0
    
    displays = [mainMenu, gameUI, paused]
    
    
    
    running = True
    
    while running:
        
        ret = displays[activeDisplay].draw()
        if ret != None:
            activeDisplay = ret
        
        pygame.display.update()
        gameClock.tick(FPS)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE and activeDisplay == 1:
                    activeDisplay = 2
                
                elif event.key == K_ESCAPE and activeDisplay == 2:
                    activeDisplay = 1

                elif event.key == K_UP and activeDisplay == 1:
                    gameUI.moveView(UP)
                    
                elif event.key == K_DOWN and activeDisplay == 1:
                    gameUI.moveView(DOWN)
                    
                elif event.key == K_LEFT and activeDisplay == 1:
                    gameUI.moveView(LEFT)

                elif event.key == K_RIGHT and activeDisplay == 1:
                    gameUI.moveView(RIGHT)
                
                elif event.key == K_r and activeDisplay == 1:
                    if game.selectedTile:
                        if game.selectedTile.unit:
                            game.selectedTile.unit.resetMoves()
                            gameUI.taskbar.updateTexts()






main()


