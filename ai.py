from player import Player
from random import randint

LEADERTAG = 1



class AI(Player):
    
    def __init__(self, ID, startTile, game):
        
        Player.__init__(self, ID, startTile, game)
        pass
    
    
    def evaluateMap(self):
        
        pass
    
    
    
    def createTask(self, unit):
        
        pass
    
    
    
    def processTurn(self):
        
        i = 0
        movesSum = 0
        previousMoves = -1
        iters = 3
        
        while self.actionsLeft() and iters:
            
            print("\n\n-------------")
            print("New iteration")
            print("-------------\n\n")
            
            for unit in self.units:
                
                print("unit moves before: {}".format(unit.moves))
                
                if unit.moves:
                    distance = self.estimatedDistance(5, unit)
                    
                    if not distance:
                        i+=1
                        movesSum += unit.moves
                        print("unit moves after: {}".format(unit.moves))
                        print("unit {}/{} done".format(i, len(self.units)))
                        print()
                        
                        continue
                    
                    distance = len(distance)
                    
                    
                    if distance > 8:
                        print("Approaching")
                        self.approachEnemy(unit)
                    
                    else:
                        print("Attacking")
                        self.attackNearestEnemy(unit)
                    
                    
                    movesSum += unit.moves
                    
                i+=1
                    
                print("unit moves after: {}".format(unit.moves))
                print("unit {}/{} done".format(i, len(self.units)))
                print()
            
            i = 0
            
            print("total moves left: {}".format(movesSum))
            
            if previousMoves == movesSum:
                iters -= 1
                
            previousMoves = movesSum
            movesSum = 0
            
            
        
        
        self.resetUnits()
        self.untagUnits()
        
        
    def untagUnits(self):   
        for unit in self.units:
            unit.tag = None
    

    def estimatedDistance(self, iters = 3, unit = None):
        
        '''
        Get [iters] random unit coords from both players, average their position,
        then calculate distance between the averages.
        Alternatively use a unit for start of the path.
        
        Returns: Estimated length between both players' armies (int)
        '''
        
        coordList = []
        
        for i in range(iters):
            rand1 = randint(0, len(self.units)-1)
            rand2 = randint(0, len(self.game.player1.units)-1)
            
            x1 = self.units[rand1].x
            y1 = self.units[rand1].y
            
            x2 = self.game.player1.units[rand2].x
            y2 = self.game.player1.units[rand2].y
            
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
        
        
        if unit:
            path = self.game.findPath( self.game.map[unit.y][unit.x], tile2 )
            return path
        else:
            path = self.game.findPath(tile1, tile2)
            return len(path)
        
        
        
        
        
        
            
            
    def findNearestEnemy(self, unit, interval = 2, maxDist = 10):
        
        '''
        Iterates around [unit]'s tiles until finds enemy unit or has searched
        over 10 tiles around the unit
        
        Returns: [tile] with unit if found or None
        '''
        
        offset = interval
        
        while offset < maxDist:
            for j in range(unit.y - offset, unit.y + offset):
                for i in range(unit.x - offset, unit.x + offset):
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
        
        
        
        
        
    def moveNearUnit(self, unit, target, distance = None):
        
        ''' Moves [unit] as close to [target] as needed for it to attack '''
        
        if not distance:
            distance = unit.range
        
        targetTile = self.findNearestPathable(target)
        
        path = self.game.findPath(self.game.map[unit.y][unit.x], targetTile)
        
        if len(path) == 0:
            unit.moves = 0
        
        indexOffset = distance if distance < len(path) else len(path)
        print("indexOffset: {} pathlen: {}".format(indexOffset, len(path)))
        if len(path):
            self.game.moveUnit(self.game.map[unit.y][unit.x], path[0-indexOffset])
        

    
    
    def approachEnemy(self, unit):
        
        '''
        Moves [unit] towards enemy army. Makes the units assign and follow a leader
        to move in a group.
        '''
        
        leader = None
        for troop in self.units:
            if troop.tag == LEADERTAG:
                leader = troop
        
        
        
        if not leader:
            unit.tag = LEADERTAG
            path = self.estimatedDistance(5, unit)
            
            if not path:
                return
            
            dist = unit.moves if unit.moves < len(path) else len(path) - 1
            print("gonna lead")
            self.game.moveUnit(self.game.map[unit.y][unit.x], path[dist])
            
        else:
            print("gonna move")
            self.moveNearUnit(unit, leader, 0)
            
    

    
    
    def attackNearestEnemy(self, unit):
        
        ''' Finds nearest enemy unit and attacks it once, if fails then moves closer'''
        
        target = self.findNearestEnemy(unit, 1)
        
        if target:
            if not self.game.dealDamage(self.game.map[unit.y][unit.x], target):
                self.moveNearUnit(unit, target)
                
        
        
        
    def retreat(self, unit):
        
        reason = self.findNearestEnemy(unit, 1)
        
        
        
        
        





