from tile import Tile
from player import Player
from unit import Unit
from random import randint


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
        self.player2 = Player(2, self.p2start, self)
        self.activeplayer = None
        self.inactiveplayer = None
        
        self.selectedTile = None
        
        
        self.initializeUnits(self.player1)
    
    
        
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
        
        
        player.colorizeUnits()
    

    
    
    def distance(self, tile1, tile2):
            return abs(tile1.x - tile2.x) + abs(tile1.y - tile2.y)    
        
    
    def moveUnit(self, sourceTile, targetTile):
        
        if not sourceTile or not targetTile.pathable:
            return
        
        if not sourceTile.unit:
            return
        
        if not sourceTile.unit.moves:
            return
        
        
        path = self.findPath(sourceTile, targetTile)
        dist = self.distance(sourceTile, targetTile)
        if  dist <= sourceTile.unit.moves and path != None:
            
            sourceTile.unit.moves -= dist
            dist -= 1
            sourceTile.unit.x, sourceTile.unit.y = path[dist].x, path[dist].y
            sourceTile.unit, path[dist].unit = path[dist].unit, sourceTile.unit
            self.selectedTile.pathable  = True
            self.selectedTile = path[dist]
        
        elif path != None and sourceTile.unit.moves > 0:
            
            tempmoves = sourceTile.unit.moves - 1
            sourceTile.unit.moves = 0
            sourceTile.unit.x, sourceTile.unit.y = path[tempmoves].x, path[tempmoves].y
            sourceTile.unit, path[tempmoves].unit = path[tempmoves].unit, sourceTile.unit
            self.selectedTile.pathable  = True
            self.selectedTile = path[tempmoves]
        
        
        
    
    
    
    def dealDamage(self, sourceTile, targetTile):
        
        if not sourceTile or not targetTile:
            return
        
        if not sourceTile.unit:
            return
        
        if not sourceTile.unit.moves:
            return
        
        
        dist = self.distance(sourceTile, targetTile)
        if  dist <= sourceTile.unit.range:
            
            sourceTile.unit.moves -= 1
            targetTile.unit.hp -= sourceTile.unit.dmg
            
            print("Target hp left:", targetTile.unit.hp)
        
        if targetTile.unit.hp <= 0:
            
            if targetTile.unit.playerID == 1:
                self.player1.units.remove(targetTile.unit)
                targetTile.unit = None
            elif targetTile.unit.playerID == 2:
                self.player2.units.remove(targetTile.unit)
                targetTile.unit = None
                targetTile.pathable = True
    
    
    
    
    
    
    def processTurn(self, player):
        pass
        
    
    
    
    
        
    
    
    
    
    
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
        
        return neighbours
    
    
    def resetTiles(self):
        
        for i in range(self.ysize):
            for j in range(self.xsize):
                self.map[i][j].visited = False
                self.map[i][j].previous = None
    
    
    
    def findPath(self, start, goal):
        
        # Greedy best-first search
        
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
                    
                print("Found", len(path), "tiles long path after", iters, "iterations")
                self.resetTiles()
                return list(reversed(path))
                
            
            activeTiles.extend(self.getNeighbours(activeTiles[0][0], goal))
            activeTiles.pop(0)
            activeTiles = sorted(activeTiles, key=getKey)
            iters += 1
            
        self.resetTiles()
        return None
    
    
    
    
    
    