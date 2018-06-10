import pygame , sys, numpy, random
from math import *
from pygame.locals import *

pygame.init()
windowWidth = 800
windowHeight = 800
displaySurf = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption('Asteroids')
fpsClock = pygame.time.Clock()
FPS = 5 # set frame rate to 30 per second
black = (0 , 0 , 0)
white = (255, 255, 255)

#Initialize game state ----------------------------------------

class Ship():
    def __init__(self):
        self.x = 100 # meters
        self.y = 100 # meters
        self.mass = 100 #kg
        self.xVelocity = 0 # meters per second
        self.yVelocity = 0 # meters per second
        self.thrust = 0 # newtons
        self.angle = 3*(pi/2) # radians

class Asteroid():
    def __init__(self):
        self.x = random.randint(0,windowWidth)
        self.y = random.randint(0,windowHeight)
        self.xVelocity = random.randint(-5,5)
        self.yVelocity = random.randint(-5,5)
        self.asteroidTemplate = [     
            [30,30,0,-30,-10,10],
            [-8,14,30,0,-60,-60]]
        self.A = [
            [0,0,0,0,0,0],
            [0,0,0,0,0,0]]
        self.asteroidPoints = 0

    def draw(self):
        #update game state
        self.x = (self.x + self.xVelocity) % windowWidth #adjust center of asteroid
        self.y = (self.y + self.yVelocity) % windowHeight
        for x in range(0,len(self.asteroidTemplate[0])): #adjust template to actual points
            self.A[0][x] = self.asteroidTemplate[0][x] + self.x
            self.A[1][x] = self.asteroidTemplate[1][x] + self.y
        self.asteroidPoints = ((self.A[0][0],self.A[1][0]),(self.A[0][1],self.A[1][1]),(self.A[0][2],self.A[1][2]),(self.A[0][3],self.A[1][3]),(self.A[0][4],self.A[1][4]),(self.A[0][5],self.A[1][5]))
        #draw
        pygame.draw.polygon(displaySurf, white, self.asteroidPoints, 1) #draw asteroid

ship = Ship()
a1 = Asteroid()
a2 = Asteroid()
a3 = Asteroid()

#points relative to center of ship, while ship is at angle: 0
shipAt0 = numpy.array([     #Points of the ship when it's facing straight east (zero degrees)
    [25,-25,-15,-25,-20,-35,-20],
    [0,14,0,-14,7,0,-7]])
rotationMatrix = numpy.array([
    [cos(ship.angle),-1*sin(ship.angle)],
    [sin(ship.angle),cos(ship.angle)]])



##### MAIN GAME LOOP ##################
while True:
    #keyboard input ------------------------------------------
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.key == 119:
                ship.thrust = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] == 1:
        ship.thrust += .3
    if keys[pygame.K_a] == 1:
        ship.angle -= pi/30
    if keys[pygame.K_d] == 1:
        ship.angle += pi/30

    #adjust game state --------------------------------------
    #SHIP
    #move ship center
    ship.xVelocity += ship.thrust*cos(ship.angle)/(ship.mass) # calculate X velocity
    ship.yVelocity += ship.thrust*sin(ship.angle)/(ship.mass) # add on the acceleration ( a = f/m)
    ship.x = (ship.x+ship.xVelocity) % windowWidth
    ship.y = (ship.y+ship.yVelocity) % windowHeight

    #calculate new points
    rotationMatrix[0][0] = cos(ship.angle)
    rotationMatrix[0][1] = -1*sin(ship.angle)
    rotationMatrix[1][0] = sin(ship.angle)
    rotationMatrix[1][1] = cos(ship.angle)
    
    points = rotationMatrix.dot(shipAt0)
    shipPoints = ((ship.x+points[0][0],ship.y+points[1][0]) , (ship.x+points[0][1],ship.y+points[1][1]) , (ship.x+points[0][2],ship.y+points[1][2]) , (ship.x+points[0][3],ship.y+points[1][3]))
    flamePoints = ((ship.x+points[0][4],ship.y+points[1][4]),(ship.x+points[0][5],ship.y+points[1][5]),(ship.x+points[0][6],ship.y+points[1][6]))    
    
 
    #draw game -----------------------------------------------
    displaySurf.fill(black) #blank the screen first
    pygame.draw.polygon(displaySurf, white, shipPoints , 1) #(surface to draw to, color, coordinates, width)
    if keys[pygame.K_w] == 1:
        pygame.draw.lines(displaySurf, white,(0,0), flamePoints, 1) 

    a1.draw()
    a2.draw()
    a3.draw()
    
    pygame.display.update()
    fpsClock.tick()
