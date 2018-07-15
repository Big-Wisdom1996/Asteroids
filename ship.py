from math import *
from numpy import *
from pygame import *

class Ship:
    def __init__(self, color,windowWidth,windowHeight):
        self.x = windowWidth/2 # meters
        self.y = windowHeight/2 # meters
        self.mass = 100 #kg
        self.xVelocity = 0 # meters per second
        self.yVelocity = 0 # meters per second
        self.thrust = 0 # newtons
        self.angle = 3*(pi/2) # radians
        #points relative to center of ship, while ship is at angle: 0
        self.shipAt0 = array([     #Points of the ship when it's facing straight east (zero degrees)
            [25,-25,-15,-25,-20,-35,-20],
            [0,14,0,-14,7,0,-7]])
        self.rotationMatrix = array([
            [cos(self.angle),-1*sin(self.angle)],
            [sin(self.angle),cos(self.angle)]])
        self.points = 0
        self.shipPoints = 0 
        self.flamePoints = 0
        self.color = color
        

    def draw(self,displaySurf,windowWidth,windowHeight,color):
        #SHIP
        #move ship center
        self.xVelocity += self.thrust*cos(self.angle)/(self.mass) # calculate X velocity
        self.yVelocity += self.thrust*sin(self.angle)/(self.mass) # add on the acceleration ( a = f/m)
        self.x = (self.x+self.xVelocity) % windowWidth
        self.y = (self.y+self.yVelocity) % windowHeight

        #calculate new points
        self.rotationMatrix[0][0] = cos(self.angle)
        self.rotationMatrix[0][1] = -1*sin(self.angle)
        self.rotationMatrix[1][0] = sin(self.angle)
        self.rotationMatrix[1][1] = cos(self.angle)
    
        self.points = self.rotationMatrix.dot(self.shipAt0)
        self.shipPoints = ((self.x+self.points[0][0],self.y+self.points[1][0]) , (self.x+self.points[0][1],self.y+self.points[1][1]) , (self.x+self.points[0][2],self.y+self.points[1][2]) , (self.x+self.points[0][3],self.y+self.points[1][3]))
        self.flamePoints = ((self.x+self.points[0][4],self.y+self.points[1][4]),(self.x+self.points[0][5],self.y+self.points[1][5]),(self.x+self.points[0][6],self.y+self.points[1][6]))    
    
        draw.polygon(displaySurf, self.color, self.shipPoints , 1) #(surface to draw to, color, coordinates, width)
        keys = key.get_pressed()
        if keys[K_w] == 1:
            draw.lines(displaySurf, color,(0,0), self.flamePoints, 1) 

    def check(self, asteroid):
        if asteroid.shape == 1:
            asteroidImpactDistance = 40
        elif asteroid.shape == 2:
            asteroidImpactDistance = 25
            
        distance = sqrt((asteroid.x - self.x)**2+(asteroid.y-self.y)**2)
        if distance < asteroidImpactDistance:
            return asteroid
        else:
            return None
