
class Arrow(object):
    weight = 22.68 # grams
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v0 = 0
        self.IBO = 105.16 # m/s
        self.addWeight = 1.296 # g
        self.drawWeight = 31751 # g 
        self.arrowWeight = 22.68 # g
    
    def findInitialSpeed(self, power):
        # v = IBO + (L - 30) * 10 - W / 3 + min (0, -(A - 5D)/3)
        # assume that additional weigth on string (W) and draw weight (D) are constant values
        # power is propotional to the draw length 
        # assume that peak draw is a constant 70 lbs
        self.v0 = self.IBO + (L - 30) * 10 - self.addWeight / 3 + min (0, -(self.arrowWeight - 5*self.drawWeight)/3)
        
    
class Target(object):
    sizeOfRings = 10 # pixels
    sizeOfInnerRing = 5 # pixels
    def __init__(self, rings):
        self.x = 0
        self.y = 0
        self.rings = rings
    
    def generateRandomLocation(self, xRange, yRange):
        x = random.randint(xRange[0], xRange[1])
        y = random.randint(yRange[0], yRange[1])
        self.x = x
        self.y = y
        return
    

