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
        self.xVelocity = random.randint(-7,7)
        self.yVelocity = random.randint(-7,7)

ship = Ship()
a1 = Asteroid()

#points relative to center of ship, while ship is at angle: 0
shipAt0 = numpy.array([     #Points of the ship when it's facing straight east (zero degrees)
    [25,-25,-15,-25,-20,-35,-20],
    [0,14,0,-14,7,0,-7]])
rotationMatrix = numpy.array([
    [cos(ship.angle),-1*sin(ship.angle)],
    [sin(ship.angle),cos(ship.angle)]])

asteroidTemplate = numpy.array([     
    [30,30,0,-30,-10,10],
    [-8,14,30,0,-60,-60]])
A = numpy.array([
    [0,0,0,0,0,0],
    [0,0,0,0,0,0]])







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

    #ASTEROID
    a1.x = (a1.x + a1.xVelocity) % windowWidth
    a1.y = (a1.y + a1.yVelocity) % windowHeight
    
    for x in range(0,len(asteroidTemplate[0])):
        A[0][x] = asteroidTemplate[0][x] + a1.x
        A[1][x] = asteroidTemplate[1][x] + a1.y
        

    asteroidPoints = ((A[0][0],A[1][0]),(A[0][1],A[1][1]),(A[0][2],A[1][2]),(A[0][3],A[1][3]),(A[0][4],A[1][4]),(A[0][5],A[1][5]))

    #draw game -----------------------------------------------
    displaySurf.fill(black) #blank the screen first
    pygame.draw.polygon(displaySurf, white, shipPoints , 1) #(surface to draw to, color, coordinates, width)
    if keys[pygame.K_w] == 1:
        pygame.draw.lines(displaySurf, white,(0,0), flamePoints, 1) 

    pygame.draw.polygon(displaySurf, white, asteroidPoints, 1)
    
    pygame.display.update()
    fpsClock.tick()
