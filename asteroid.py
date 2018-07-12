import random
from pygame import draw
from math import sqrt

class Asteroid:
    def __init__(self, windowWidth, windowHeight):
        side = random.randint(1,4)
        if side == 1:
            self.x = random.randint(0, windowWidth)
            self.y = 0
        elif side == 2:
            self.x = windowWidth
            self.y = random.randint(0, windowHeight)
        elif side == 3:
            self.x = random.randint(0, windowWidth)
            self.y = windowHeight
        elif side == 4:
            self.x = 0
            self.y = random.randint(0,windowHeight)

        self.xVelocity = random.randint(-5,5)
        self.yVelocity = random.randint(-5,5)
        self.asteroidTemplate = [     
            [30,30,0,-30,-10,10],
            [2,24,40,10,-45,-45]]
        self.points = ['','','','','','']

    def draw(self, displaySurf, color, windowWidth, windowHeight):
        for x in range(0,len(self.asteroidTemplate[0])):
            self.points[x] = (self.x+self.asteroidTemplate[0][x],self.y+self.asteroidTemplate[1][x])

        draw.polygon(displaySurf, color, self.points, 1)
        self.x = (self.x + self.xVelocity) % windowWidth #adjust center of asteroid
        self.y = (self.y + self.yVelocity) % windowHeight

    def checkLasers(self, lasers, laserImpactDistance):
        for laser in lasers:
            distance = sqrt((laser.points[2] - self.x)**2 + (laser.points[3] - self.y)**2)
            if distance < laserImpactDistance:
                return laser
        return None
