import pygame

# Color constants
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
LGREEN= (100, 255, 100)
RED =   (255,   0,   0)
LRED =  (255, 100, 100)


# Visual constants
TASKBARHEIGHT = 152
TILESIZE = 32


# Movement constants
UP    = ( 0 , 1)
DOWN  = ( 0 ,-1)
LEFT  = ( 1 , 0)
RIGHT = (-1 , 0)
DIRECTIONS = (UP, DOWN, LEFT, RIGHT)




class Taskbar:
    
    def __init__(self, screen):
        
        self.screen = screen
        
        self.x = 0
        self.y = self.screen.get_height() - TASKBARHEIGHT
        self.width = self.screen.get_width()
        self.height = TASKBARHEIGHT

    def draw(self):
        
        pygame.draw.rect(self.screen, BLACK, (self.x,self.y,self.width,self.height))
    


class Gameview:
    
    def __init__(self, screen, game):
        
        self.screen = screen
        self.game = game
        self.viewx = int( self.screen.get_width() / TILESIZE )
        self.viewy = int( ( self.screen.get_height() - TASKBARHEIGHT ) / TILESIZE )
        
        
        self.mapx = self.game.xsize
        self.mapy = self.game.ysize
        
        self.currentx = 0
        self.currenty = 0
        
        
        
    def draw(self):
        
        for i in range(self.viewy):
            for j in range(self.viewx):
                
                self.screen.blit(pygame.transform.scale( self.game.map[i+self.currenty][j+self.currentx].img, (TILESIZE,TILESIZE)), \
                                 (j * TILESIZE, i * TILESIZE))
                
                if self.game.map[i+self.currenty][j+self.currentx].unit:
                    
                    self.screen.blit(self.game.map[i+self.currenty][j+self.currentx].unit.img, \
                                 (j * TILESIZE, i * TILESIZE))
    

    
    
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
        
    
    
    
    
    

class UI:
    
    def __init__(self, screen, game):
        
        self.game = game
        self.screen = screen
        
        self.taskbar = Taskbar(self.screen)
        self.gameview = Gameview(self.screen, self.game)
        
        self.objects = [self.taskbar, self.gameview]


    def draw(self):
        
        
        #self.screen.fill(BLACK)
        for thing in self.objects:
            thing.draw()

        return 1

