

class Player:
    
    def __init__(self):

        self.units = []
    
    
    
    def actionsLeft(self):
        
        for unit in self.units:
            if unit.moves > 0:
                return True
        
        return False
    
    
    
    def resetUnits(self):
        
        for unit in self.units:
            unit.resetMoves()
