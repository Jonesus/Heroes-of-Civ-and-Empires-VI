LANDSCAPES = {"M":(False, "pathtoimg"), "G":(True, "pathtoimg"), "W":(False, "pathtoimg")}



class Tile:
    
    def __init__(self, x, y, landscape):
        
        self.x = x
        self.y = y
        self.unit = None
        
        self.pathable = LANDSCAPES[landscape[0]]
        self.img      = LANDSCAPES[landscape[1]]
        
        
        