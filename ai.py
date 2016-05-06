from player import Player
from random import randint

LEADERTAG = 1



class AI(Player):
    
    '''
    Represents the artificial intelligence opponent to play against.
    Inherits variables and methods from Player class
    
    Methods:
    processTurn(): evaluates the current position for each unit and either
                   moves closer or attacks the nearest opponent's unit
    estimatedDistance(): Estimates the distance of either both player's armies
                         or a single unit and the opponent's army
    findNearestEnemy(): Finds the nearest enemy unit
    findNearestPathable(): Finds the nearest pathable tile
    moveNearUnit(): Moves unit as close to the enemy as it needs to be to attack
    approachEnemy(): Makes the units approach enemy's army
    attackNearestEnemy(): Well duh
    
    '''
    
    
    
    
    
    def __init__(self, ID, startTile, game):
        
        Player.__init__(self, ID, startTile, game)

    
    def processTurn(self):
        
        uniti = 0
        movesSum = 0
        previousMoves = -1
        iters = 3
        
        while self.actionsLeft() and iters:
            
            #print("\n\n-------------")
            #print("New iteration")
            #print("-------------\n\n")
            
            
            for i in range(self.game.ysize):
                for j in range(self.game.xsize):
                    if self.game.map[i][j].unit:
                        if self.game.map[i][j].unit.playerID == 2:
                            
                            tile = self.game.map[i][j]
                            unit = self.game.map[i][j].unit
                            
                            
                            #print("Unit: {}".format(unit.name))
                            #print("unit moves before: {}".format(tile.unit.moves))
                            
                            
                            if tile.unit.moves:
                                distance = self.estimatedDistance(5, tile)
                                
                                if distance == -1:
                                    return -1
                                
                                if not distance:
                                    #print("Couldn't get distance!")
                                    uniti+=1
                                    movesSum += tile.unit.moves
                                    #print("unit moves after: {}".format(tile.unit.moves))
                                    #print("unit {}/{} done".format(uniti, len(self.units)))
                                    #print()
                                    
                                    continue
                                
                                distance = len(distance)
                                #print("Est.dist. {}".format(distance))
                                
                                if distance > 10:
                                    #print("Approaching")
                                    self.approachEnemy(tile)
                                
                                else:
                                    #print("Attacking")
                                    self.attackNearestEnemy(tile)
                                
                                
                                movesSum += unit.moves
                                
                            uniti+=1
                    
                            #print("unit moves after: {}".format(unit.moves))
                            #print("unit {}/{} done".format(uniti, len(self.units)))
                            #print()
            
            uniti = 0
            
            #print("total moves left: {}".format(movesSum))
            
            if previousMoves == movesSum:
                iters -= 1
                
            previousMoves = movesSum
            movesSum = 0
            
            
        
        
        self.resetUnits()
        self.game.untagUnits(self)
        
        
    

    def estimatedDistance(self, iters = 3, tile = None):
        
        '''
        Get [iters] random unit coords from both players, average their position,
        then calculate distance between the averages.
        Alternatively use a unit for start of the path.
        
        Returns: Estimated length between both players' armies (int)
        '''
        
        p1unitCoords = []
        p2unitCoords = []
        
        for i in range(self.game.ysize):
            for j in range(self.game.xsize):
                if self.game.map[i][j].unit:
                    if self.game.map[i][j].unit.playerID == 1:
                        p1unitCoords.append((j,i))
                    else:
                        p2unitCoords.append((j,i))
        
        
        if len(p1unitCoords) == 0 or len(p2unitCoords) == 0:
            return -1
        
        
        coordList = []
        
        for i in range(iters):
            rand1 = randint(0, len(p1unitCoords)-1)
            rand2 = randint(0, len(p2unitCoords)-1)
            
            x1 = p1unitCoords[rand1][0]
            y1 = p1unitCoords[rand1][1]
            
            x2 = p2unitCoords[rand2][0]
            y2 = p2unitCoords[rand2][1]
            
            coordList.append( ((x1,y1),(x2,y2)) )
        
        x1sum = x2sum = y1sum = y2sum = 0
        
        for i in range(iters):
            x1sum += coordList[i][0][0]
            y1sum += coordList[i][0][1]
            x2sum += coordList[i][1][0]
            y2sum += coordList[i][1][1]
            
        x1sum = x1sum // iters
        y1sum = y1sum // iters
        x2sum = x2sum // iters
        y2sum = y2sum // iters
        
        tile1 = self.findNearestPathable(self.game.map[y1sum][x1sum])
        tile2 = self.findNearestPathable(self.game.map[y2sum][x2sum])
        
        
        if tile:
            path = self.game.findPath(tile, tile1)
            return path
        else:
            path = self.game.findPath(tile2, tile1)
            return len(path)
        
        
        
        
        
        
            
            
    def findNearestEnemy(self, tile, interval = 2, maxDist = 10):
        
        '''
        Iterates around [unit]'s tiles until finds enemy unit or has searched
        over 10 tiles around the unit
        
        Returns: [tile] with unit if found or None
        '''
        
        offset = interval
        
        while offset < maxDist:
            for j in range(tile.y - offset, tile.y + offset):
                for i in range(tile.x - offset, tile.x + offset):
                    if i < self.game.xsize and i >= 0 \
                    and j < self.game.ysize and j >= 0:
                        if self.game.map[j][i].unit:
                            if self.game.map[j][i].unit.playerID == 1:
                                return self.game.map[j][i]
            
            offset += interval
        
        return None
        
    
    
    def findNearestPathable(self, target):
        
        '''
        Iterates around [unit]'s tiles until finds pathable tile or has searched
        over 10 tiles around the unit
        
        Returns: [tile] if found or None
        '''
        
        offset = 1
        
        while offset < 10:
            for j in range(target.y - offset, target.y + offset):
                for i in range(target.x - offset, target.x + offset):
                    if self.game.map[j][i].pathable:
                        return self.game.map[j][i]
            
            offset += 1
        
        return None
        
        
        
        
        
    def moveNearUnit(self, unitTile, target, distance = None):
        
        ''' Moves [unit] as close to [target] as needed for it to attack '''
        
        if not distance:
            distance = unitTile.unit.range
        
        targetTile = self.findNearestPathable(target)
        
        path = self.game.findPath(unitTile, targetTile)
        
        if not path:
            return
        
        if len(path) == 0:
            unitTile.unit.moves = 0
        
        indexOffset = distance if distance < len(path) else len(path)
        #print("indexOffset: {} pathlen: {}".format(indexOffset, len(path)))
        if len(path):
            self.game.moveUnit(unitTile, path[0-indexOffset])
        

    
    
    def approachEnemy(self, unitTile):
        
        '''
        Moves [unit] towards enemy army. Makes the units assign and follow a leader
        to move in a group.
        '''
        
        leaderTile = None
        for i in range(self.game.ysize):
                for j in range(self.game.xsize):
                    if self.game.map[i][j].unit:
                        if self.game.map[i][j].unit.playerID == 2 \
                        and self.game.map[i][j].unit.tag == LEADERTAG:
                            leaderTile = self.game.map[i][j]
        
        
        
        if not leaderTile:
            unitTile.unit.tag = LEADERTAG
            path = self.estimatedDistance(5, unitTile)
            
            if not path:
                return
            
            dist = unitTile.unit.moves if unitTile.unit.moves < len(path) else len(path) - 1
            #print("New leader")
            self.game.moveUnit(unitTile, path[dist])
            
        else:
            #print("Moving towards leader")
            self.moveNearUnit(unitTile, leaderTile, 0)
            
    

    
    
    def attackNearestEnemy(self, unitTile):
        
        ''' Finds nearest enemy unit and attacks it once, if fails then moves closer'''
        
        target = self.findNearestEnemy(unitTile, interval = 1, maxDist = 12)
        
        print("Distance from target: {}".format(self.game.distance(unitTile, target)))
        
        if target:
            if not self.game.dealDamage(unitTile, target):
                #print("Moving closer")
                self.moveNearUnit(unitTile, target)
                
        
        
        
        
        
        
        
        





