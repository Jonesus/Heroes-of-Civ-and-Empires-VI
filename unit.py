


class unit:
    
    def __init__(self, x, y, source):
        
        file = open(source, 'r')
        attributelist = {}
        
        for line in file:
            linelist = line.split(';')
            attributelist[ linelist[0] ] = linelist[1]
        
        self.x = x
        self.y = y
        self.name = attributelist["name"]
        self.hp = attributelist["hp"]
        self.dmg = attributelist["dmg"]
        self.range = attributelist["range"]
        self.moves = attributelist["moves"]
        
        
        
        
        