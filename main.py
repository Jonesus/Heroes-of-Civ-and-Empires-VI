import pygame
from menu import Menu




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
    
    
    mainMenu = Menu(gameScreen)
    
    
    
    
    
    running = True
    
    while running:
        
        mainMenu.draw()
        
        pygame.display.update()
        gameClock.tick(FPS)
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
















main()


