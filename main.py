import pygame
from pygame.locals import *


from menu import Menu
from ui import Gameview, Pauseview, Gameover
from game import Game

UP    = ( 0 ,-1)
DOWN  = ( 0 , 1)
LEFT  = (-1 , 0)
RIGHT = ( 1 , 0)


DEFAULTWIDTH = 800
DEFAULTHEIGHT = 600
DEFAULTFPS = 30
DEFAULTP1COLOR = (  0,  0, 255)
DEFAULTP2COLOR = (255,  0,   0)






def parseSetup():
    
    setupDict = {}
    
    with open("setup.txt", "r") as file:
        for line in file:
            if line[0] == "#" or line[0] == "\n":
                continue
            
            linelist = line.rstrip().split(":")
            setupDict[ linelist[0] ] = linelist[1]
            
    return setupDict
    
    
    
    

def main():
    
    # Initialize all pygame constants and variables
    
    pygame.display.init()
    pygame.init()
    
    displayWidth = DEFAULTWIDTH
    displayHeight = DEFAULTHEIGHT
    FPS = DEFAULTFPS
    
    
    setup = parseSetup()
    

    
    try:
        if int(setup["width"]) > 400:
            displayWidth = int(setup["width"])
            
        if int(setup["height"]) > 300:
            displayHeight = int(setup["height"])
        
        if int(setup["fps"]) > 10:
            FPS = int(setup["fps"])
            
    except ValueError:
        print("Invalid options file, resetting to defaults")
        displayWidth = DEFAULTWIDTH
        displayHeight = DEFAULTHEIGHT
        FPS = DEFAULTFPS
        
    else:
        print("Game options set up correctly.")

    screenSize = (displayWidth, displayHeight)
    
    gameScreen = pygame.display.set_mode(screenSize)
    gameClock = pygame.time.Clock()
    pygame.display.set_caption("Heroes of Civ and Empires VI")
    
    # Initialize the game itself, read default file for map
    
    mapsyntax = []
    
    try:
        i = 1
        while i <= int(setup["landtypes"]):
            line = setup["land{}".format(i)].split(";")
            line[1] = line[1].split(" ")
            mapsyntax.append(line)
            i = i+1
    
    except ValueError:
        print("Failed to read map syntax, illegal values in file!")
        quit()
        
        
    except KeyError:
        print("Failed to read map syntax, illegal keys in file!")
        quit()
        
    else:
        print("Map syntax successfully parsed.")
    
    
    
    
    try:
        colors1 = setup["player1color"].split(" ")
        colors2 = setup["player2color"].split(" ")
        
        for color in colors1:
            color = int(color)
            if color > 255 or color < 0:
                raise ValueError
            
        for color in colors2:
            color = int(color)
            if color > 255 or color < 0:
                raise ValueError
        
        player1color = (int(colors1[0]), int(colors1[1]), int(colors1[2]))
        player2color = (int(colors2[0]), int(colors2[1]), int(colors2[2]))
    
    except KeyError:
        print("Invalid player color keys in setup file!")
        print("Resetting to defaults.")
        player1color = DEFAULTP1COLOR
        player2color = DEFAULTP2COLOR
        
    except ValueError:
        
        print("Invalid player color values in setup file!")
        print("Resetting to defaults.")
        player1color = DEFAULTP1COLOR
        player2color = DEFAULTP2COLOR
        
    else:
        print("Player colors read successfully.")
    
    game = Game(setup["mapfile"], mapsyntax, player1color, player2color)
    
    try:
        game = Game(setup["mapfile"], mapsyntax, player1color, player2color)
        gameparams = [setup["mapfile"], mapsyntax, player1color, player2color]
    
    except KeyError:
        print("No map file specified in setup.txt!")
        quit()
    
    # Initialize 
    
    mainMenu = Menu(gameScreen, game, gameparams)
    
    paused = Pauseview(gameScreen, game)
    over = Gameover(gameScreen, game)
    
    try:
        gameUI = Gameview(gameScreen, game, over, int(setup["tilesize"]))
    except ValueError:
        print("Invalid tilesize in setup.txt!")
        print("Resetting to defaults.")
        gameUI = Gameview(gameScreen, game, over, 32)
        
    activeDisplay = 0
    
    displays = [mainMenu, gameUI, paused, over]
    
    
    
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


