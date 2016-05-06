from tile import Tile
from player import Player
from ai import AI
from unit import Unit
from random import randint


BLUE = (  0,   0, 255)
RED  = (255,   0,   0)

class Game:
    
    '''
    Represents the current instance of the game.
    
    Params:
    mapfile: path to .txt file containing the map
    
    Attributes:
    map: 2D array of tiles which forms the game map
    xsize: width of the game map in tiles
    ysize: height of the game map in tiles
    p#start: starting tile for player
    player#: instance of a player class
    
    Methods:
    generateMap(): reads the map file and creates a 2D array of tiles according to file
    initializeUnits(): reads a player file which describes what kind of army each player has
    untagUnits(): removes each unit's tag
    distance(): distance between two tiles
    moveUnit(): moves unit from a tile to another using greedy best-first pathfinding
    dealDamage(): makes a unit hit another
    swapPlayer(): changes the active and inactive player
    switchTurn(): changes the turn
    getNeighbours(), resetTiles(), findPath(): implementation of a greedy best-first search
    
    '''
    
    
    
    def __init__(self, mapfile, mapsyntax, p1color, p2color):
        
        
        self.map, self.xsize, self.ysize = self.generateMap(mapfile, mapsyntax)
                
        self.gameover = False
        
        self.p1start = None
        self.p2start = None
        
        self.p1color = p1color
        self.p2color = p2color
        
        try:
        
            for i in range(self.ysize):
                for j in range(self.xsize):
                    if self.map[i][j].startpos == 1:
                        self.p1start = self.map[i][j]
                    elif self.map[i][j].startpos == 2:
                        self.p2start = self.map[i][j]
                    
        except IndexError:
            print("Invalid map file!")
            print("Map not shaped properly.")
            quit()
        
        
        if not self.p1start or not self.p2start:
            print("Invalid map file!")
            print("Can't find player start positions!")
            quit()
        
        
        #TODO: raise corruptedmapfile
        
        self.player1 = Player(1, self.p1start, self)
        self.player2 = AI(2, self.p2start, self)
        self.activePlayer = self.player1
        self.inactivePlayer = self.player2
        
        self.selectedTile = None
        
        
        self.initializeUnits(self.player1)
        self.initializeUnits(self.player2)
    
    
        
    def generateMap(self, mapfile, mapsyntax):
        
        gamemap = []
        
        try:
            with open(mapfile, 'r') as file:
            
                i = j = 0
                for line in file:
                    if line[0] == "#" or line[0] == "\n":
                        continue
                    
                    gamemap.append([])
                    line = line.rstrip()
                    for char in line:
                        gamemap[i].append( Tile(j, i, char, mapsyntax) )
                        j += 1
                    xsize = j
                    j = 0
                    i += 1
                ysize = i
            
        except FileNotFoundError:
            
            with open("log.txt", "w") as out:
                out.write("Can't open map file!")
            print("Can't open map file!")
            quit()
            
        
        return gamemap, xsize, ysize
    



    
    def initializeUnits(self, player):
        
        '''
        Reads the player's army composition from a file and
        randomly distributes it around the player's starting point.
        '''
        
        try:
            with open("units/player{}.txt".format(player.ID), 'r') as file:
                
                unitcount = 0
                
                for line in file:
                    
                    if line[0] == "#" or line[0] == "\n":
                        continue
                    
                    linelist = line.split('*')
                    
                    if int(linelist[1]) > 10:
                        raise IndexError
                        
                    
                    unitcount += int(linelist[1])   
                    for i in range( int(linelist[1]) ):
                        pathToUnit = "units/" + linelist[0] + ".txt" 
                        player.units.append(Unit(player.ID, pathToUnit))
            
            
            pathablesum = 0
            for row in self.map:
                for tile in row:
                    if tile.pathable:
                        pathablesum += 1
            
            
            unitsum = 0
            if self.player1:
                if self.player1.units:
                    unitsum += len(self.player1.units)
            if self.player2:
                if self.player2.units:
                    unitsum += len(self.player2.units)
            
            if unitsum + 10 >  pathablesum:
                raise KeyError
        
        
        except KeyError:
            print("Not enough room in map for units!")
            with open("log.txt", "w") as out:
                out.write("not enough room in map for units!")
            quit()
            
            
        except:
            print("Invalid player units file!")
            with open("log.txt", "w") as out:
                out.write("Invalid player units file!")
            quit()
        
        
        
        donecount = 0
        unitrange = 1
        while donecount != unitcount:
            for i in range(unitcount):
                if not player.units[i].tag:
                    
                    temp = player.startTile.x - unitrange
                    randxmin = temp if temp > 0 else 0
                    temp = player.startTile.x + unitrange
                    randxmax = temp if temp < self.xsize else self.xsize-1
                    temp = player.startTile.y - unitrange
                    randymin = temp if temp > 0 else 0
                    temp = player.startTile.y + unitrange
                    randymax = temp if temp < self.ysize else self.ysize-1
                    
                    
                    randx = randint(randxmin, randxmax)
                    randy = randint(randymin, randymax)

                    
                    if not self.map[randy][randx].pathable:
                        continue
                        
                    self.map[randy][randx].addUnit(player.units[i])
                    self.map[randy][randx].unit.tag = 1
                    
                    donecount += 1
                    
            unitrange += 1    
        
        if player.ID == 1:
            player.colorizeUnits(self.p1color)
        elif player.ID == 2:
            player.colorizeUnits(self.p2color)
    
    
        self.untagUnits(player)
        
        
        
        
    
    def untagUnits(self, player):   
        for unit in player.units:
            unit.tag = None
            
            
            
    
    
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
            #print("Distance: {}".format(dist))
            #print("Tile coords before: {} {}".format(sourceTile.x, sourceTile.y))
            
            sourceTile.unit, path[dist].unit = path[dist].unit, sourceTile.unit
            
            #print("Tile coords after: {} {}".format(path[dist].x, path[dist].y))
            
            sourceTile.pathable = True
            path[dist].pathable = False
            self.selectedTile = path[dist]
        
        elif path != None and sourceTile.unit.moves > 0:
            
            tempmoves = sourceTile.unit.moves - 1
            sourceTile.unit.moves = 0
            
            #print("Tile coords before: {} {}".format(sourceTile.x, sourceTile.y))
            #print("Unit: {}, dest: {}".format(sourceTile.unit, path[tempmoves].unit))
            
            sourceTile.unit, path[tempmoves].unit = path[tempmoves].unit, sourceTile.unit
            
            #print("Tile coords after: {} {}".format(path[tempmoves].x, path[tempmoves].y))
            
            sourceTile.pathable = True
            path[tempmoves].pathable = False
            self.selectedTile = path[tempmoves]
        
        
        
    
    
    
    def dealDamage(self, sourceTile, targetTile):
        
        if not sourceTile or not targetTile:
            print("Shit parameters lol")
            return False
        
        if not sourceTile.unit:
            print("Shit sourcetile lol")
            return False
        
        if not sourceTile.unit.moves:
            print("No moves lol")
            return False
        
        
        dist = self.distance(sourceTile, targetTile)
        if  dist <= sourceTile.unit.range:
            
            sourceTile.unit.moves -= 1
            targetTile.unit.hp -= sourceTile.unit.dmg
            
            print("Target hp left:", targetTile.unit.hp)
        else:
            print("Not in range")
            return False
        
        
        if targetTile.unit.hp <= 0:
            
            if targetTile.unit.playerID == 1:
                print("Player 1's {} got killed!".format(targetTile.unit.name))
                self.player1.units.remove(targetTile.unit)
                targetTile.unit = None
                targetTile.pathable = True
            elif targetTile.unit.playerID == 2:
                print("Player 2's {} got killed!".format(targetTile.unit.name))
                self.player2.units.remove(targetTile.unit)
                targetTile.unit = None
                targetTile.pathable = True
    
        return True
    
    
    
    
    def swapPlayers(self):
        
        self.activePlayer, self.inactivePlayer = self.inactivePlayer, self.activePlayer
    
    
    
    def switchTurn(self):
        
        print("Switching turns\n")
        self.swapPlayers()
        if self.activePlayer.ID == 2:
            print("--------------------")
            print("--------------------")
            print("Processing AI's turn")
            print("--------------------")
            print("--------------------")
            ret = self.activePlayer.processTurn()
            print("Done")
            print("--------------------\n")
        
        if ret == -1:
            print("Game over lol")
            return 3
            
        self.swapPlayers()
        self.activePlayer.resetUnits()
        print("Player 1 active\n\n")
    
        return None
    
        
    
    
    
    
    
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
    
    
    
    
    
    