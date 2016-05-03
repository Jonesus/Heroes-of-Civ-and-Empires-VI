from tile import Tile
from player import Player
from ai import AI
from unit import Unit
from random import randint


BLUE = (  0,   0, 255)
RED  = (255,   0,   0)

class Game:
    
    def __init__(self, mapfile):
        
        
        self.map, self.xsize, self.ysize = self.generateMap(mapfile)
        
        self.p1start = None
        self.p2start = None
        
        for i in range(self.ysize):
            for j in range(self.xsize):
                if self.map[i][j].startpos == 1:
                    self.p1start = self.map[i][j]
                elif self.map[i][j].startpos == 2:
                    self.p2start = self.map[i][j]
        
        #TODO: raise corruptedmapfile
        
        self.player1 = Player(1, self.p1start, self)
        self.player2 = AI(2, self.p2start, self)
        self.activePlayer = self.player1
        self.inactivePlayer = self.player2
        
        self.selectedTile = None
        
        
        self.initializeUnits(self.player1)
        self.initializeUnits(self.player2)
    
    
        
    def generateMap(self, mapfile):
        
        gamemap = []
        
        file = open(mapfile, 'r')
        
        i = j = 0
        for line in file:
            gamemap.append([])
            line = line.rstrip()
            for char in line:
                gamemap[i].append( Tile(j, i, char) )
                j += 1
            xsize = j
            j = 0
            i += 1
        ysize = i
        
        return gamemap, xsize, ysize
    



    
    def initializeUnits(self, player):
        
        with open("units/player{}.txt".format(player.ID), 'r') as file:
            
            unitcount = 0
            
            for line in file:
                linelist = line.split('*')
                
                if int(linelist[1]) > 10:
                    #TODO: raise unitcounterror
                    return
                
                unitcount += int(linelist[1])   
                for i in range( int(linelist[1]) ):
                    pathToUnit = "units/" + linelist[0] + ".txt" 
                    player.units.append(Unit(None, None, player.ID, pathToUnit))
        
        
        
        donecount = 0
        unitrange = 1
        while donecount != unitcount:
            for i in range(unitcount):
                if not player.units[i].x:
                    randx = randint(player.startTile.x - unitrange, player.startTile.x + unitrange)
                    randy = randint(player.startTile.y - unitrange, player.startTile.y + unitrange)
                    
                    if randx < 0 or randx > self.xsize or randy < 0 or randy > self.ysize:
                        continue
                    
                    if not self.map[randy][randx].pathable:
                        continue
                        
                    self.map[randy][randx].addUnit(player.units[i])
                    player.units[i].x = randx
                    player.units[i].y = randy
                    donecount += 1
            unitrange += 1    
        
        if player.ID == 1:
            player.colorizeUnits(BLUE)
        elif player.ID == 2:
            player.colorizeUnits(RED)
    

    
    
    def distance(self, tile1, tile2):
            return abs(tile1.x - tile2.x) + abs(tile1.y - tile2.y)    
        
    
    
    
    def moveUnit(self, sourceTile, targetTile):
        
        '''
        Moves unit from [sourceTile] to [targetTile] if unit as enough moves left,
        otherwise to a tile in between the source and target.
        
        Returns: nothing
        '''
        
        if not sourceTile or not targetTile.pathable:
            print("Target tile not pathable!")
            return
        
        if not sourceTile.unit:
            print("No unit in source tile!")
            print(sourceTile.x, sourceTile.y)
            return
        
        if sourceTile.unit.moves < 1:
            print("Source tile unit has no moves!")
            print(sourceTile.unit.moves, sourceTile.x, sourceTile.y)
            return
        
        
        path = self.findPath(sourceTile, targetTile)
        dist = self.distance(sourceTile, targetTile)
        if  dist <= sourceTile.unit.moves and path != None:
            
            sourceTile.unit.moves -= dist
            dist -= 1
            
            print("Unit coords before: {} {}, tile coords before: {} {}"\
                  .format(sourceTile.unit.x, sourceTile.unit.y, sourceTile.x, sourceTile.y))
            
            sourceTile.unit.x, sourceTile.unit.y = path[dist].x, path[dist].y
            sourceTile.unit, path[dist].unit = path[dist].unit, sourceTile.unit
            
            print("Unit coords after: {} {}, tile coords after: {} {}"\
                  .format(path[dist].x, path[dist].y, path[dist].unit.x, path[dist].unit.y))
            
            sourceTile.pathable = True
            self.selectedTile = path[dist]
        
        elif path != None and sourceTile.unit.moves > 0:
            
            tempmoves = sourceTile.unit.moves - 1
            sourceTile.unit.moves = 0
            
            print("Unit coords before: {} {}, tile coords before: {} {}"\
                  .format(sourceTile.unit.x, sourceTile.unit.y, sourceTile.x, sourceTile.y))
            
            sourceTile.unit.x, sourceTile.unit.y = path[tempmoves].x, path[tempmoves].y
            sourceTile.unit, path[tempmoves].unit = path[tempmoves].unit, sourceTile.unit
            
            print("Unit coords after: {} {}, tile coords after: {} {}"\
                  .format(path[tempmoves].unit.x, path[tempmoves].unit.y, path[tempmoves].x, path[tempmoves].y))
            
            sourceTile.pathable = True
            self.selectedTile = path[tempmoves]
        
        
        
    
    
    
    def dealDamage(self, sourceTile, targetTile):
        
        if not sourceTile or not targetTile:
            return False
        
        if not sourceTile.unit:
            return False
        
        if not sourceTile.unit.moves:
            return False
        
        
        dist = self.distance(sourceTile, targetTile)
        if  dist <= sourceTile.unit.range:
            
            sourceTile.unit.moves -= 1
            targetTile.unit.hp -= sourceTile.unit.dmg
            
            print("Target hp left:", targetTile.unit.hp)
        else: 
            return False
        
        
        if targetTile.unit.hp <= 0:
            
            if targetTile.unit.playerID == 1:
                self.player1.units.remove(targetTile.unit)
                targetTile.unit = None
            elif targetTile.unit.playerID == 2:
                self.player2.units.remove(targetTile.unit)
                targetTile.unit = None
                targetTile.pathable = True
    
        return True
    
    
    
    
    def swapPlayers(self):
        
        self.activePlayer, self.inactivePlayer = self.inactivePlayer, self.activePlayer
    
    
    
    def switchTurn(self):
        
        print("Switching turns")
        self.swapPlayers()
        if self.activePlayer.ID == 2:
            print("--------------------")
            print("--------------------")
            print("Processing AI's turn")
            print("--------------------")
            print("--------------------")
            self.activePlayer.processTurn()
            print("Done")
            print("--------------------\n")
            
        self.swapPlayers()
        self.activePlayer.resetUnits()
        print("Player 1 active\n\n")
    
    
    
        
    
    
    
    
    
    def getNeighbours(self, tile, goal):
        
        neighbours = []
        
        if self.xsize > tile.x+1:
            if self.map[tile.y][tile.x+1].pathable and not self.map[tile.y][tile.x+1].visited:
                self.map[tile.y][tile.x+1].visited = True
                neighbours.append( (self.map[tile.y][tile.x+1], self.distance(self.map[tile.y][tile.x+1], goal)) )
                
        if tile.x-1 > 0:
            if self.map[tile.y][tile.x-1].pathable and not self.map[tile.y][tile.x-1].visited:
                self.map[tile.y][tile.x-1].visited = True
                neighbours.append( (self.map[tile.y][tile.x-1], self.distance(self.map[tile.y][tile.x-1], goal)) )
                   
        if self.ysize > tile.y+1:
            if self.map[tile.y+1][tile.x].pathable and not self.map[tile.y+1][tile.x].visited:
                self.map[tile.y+1][tile.x].visited = True
                neighbours.append( (self.map[tile.y+1][tile.x], self.distance(self.map[tile.y+1][tile.x], goal)) )
        
        if tile.y-1 > 0:
            if self.map[tile.y-1][tile.x].pathable and not self.map[tile.y-1][tile.x].visited:
                self.map[tile.y-1][tile.x].visited = True
                neighbours.append( (self.map[tile.y-1][tile.x], self.distance(self.map[tile.y-1][tile.x], goal)) )
        
        
        for thing in neighbours:
            thing[0].previous = tile
        
        #TODO: Finding estimated path
        
        return neighbours
    
    
    
    def resetTiles(self):
        
        for i in range(self.ysize):
            for j in range(self.xsize):
                self.map[i][j].visited = False
                self.map[i][j].previous = None
    
    
    
    def findPath(self, start, goal):
        
        '''
        Finds path between [start] and [goal] using greedy best-first search
        
        Returns: list of tiles from start to goal or None if path not found
        '''
                
        def getKey(item):
            return item[1]
        
        
        iters = 0
        path = []
        
        activeTiles = self.getNeighbours(start, goal)
        activeTiles = sorted(activeTiles, key=getKey) 
        
        
        while activeTiles:
            
            if activeTiles[0][0] == goal:
                tile = activeTiles[0][0]
                
                while tile != start:
                    path.append(tile)
                    tile = tile.previous
                    
                #print("Found", len(path), "tiles long path after", iters, "iterations")
                self.resetTiles()
                return list(reversed(path))
                
            
            activeTiles.extend(self.getNeighbours(activeTiles[0][0], goal))
            activeTiles.pop(0)
            activeTiles = sorted(activeTiles, key=getKey)
            iters += 1
            
        self.resetTiles()
        print("Can't find path!")
        return None
    
    
    
    
    
    