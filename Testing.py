import pygame , sys, numpy
from math import *
from pygame.locals import *

pygame.init()
windowWidth = 600
windowHeight = 400
displaySurf = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption('Asteroids')
fpsClock = pygame.time.Clock()
FPS = 5 # set frame rate to 30 per second
black = (0 , 0 , 0)
white = (255, 255, 255)

class Ship():
    def __init__(self):
        self.x = 100 # meters
        self.y = 100 # meters
        self.mass = 100 #kg
        self.xVelocity = 0 # meters per second
        self.yVelocity = 0 # meters per second
        self.thrust = 0 # newtons
        self.angle = 3*(pi/2) # radians

ship = Ship()
####

#points relative to center of ship, while ship is at angle: 0
shipAt0 = numpy.array([
    [25,-25,-15,-25],
    [0,15,0,-15]])

rotationMatrix = numpy.array([
    [cos(ship.angle),-1*sin(ship.angle)],
    [sin(ship.angle),cos(ship.angle)]])

points = rotationMatrix.dot(shipAt0)

shipPoints = ((ship.x+points[0][0],ship.y+points[1][0]) , (ship.x+points[0][1],ship.y+points[1][1]) , (ship.x+points[0][2],ship.y+points[1][2]) , (ship.x+points[0][3],ship.y+points[1][3]))

pygame.draw.polygon(displaySurf, white, shipPoints , 1)

##### MAIN GAME LOOP ##################
while True: 
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYUP:
            if event.unicode == 'w':
                ship.thrust = 0
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] == 1:
        ship.thrust += .1
    if keys[pygame.K_a] == 1:
        ship.angle -= pi/30
    if keys[pygame.K_d] == 1:
        ship.angle += pi/30

    #adjust center of ship
    ship.xVelocity += ship.thrust*cos(ship.angle)/(ship.mass) # calculate X velocity
    ship.yVelocity += ship.thrust*sin(ship.angle)/(ship.mass) # add on the acceleration ( a = f/m)
    ship.x = (ship.x+ship.xVelocity) % windowWidth
    ship.y = (ship.y+ship.yVelocity) % windowHeight

    #draw ship
    displaySurf.fill(black) #blank the screen first
    #calculate new points

    rotationMatrix[0][0] = cos(ship.angle)
    rotationMatrix[0][1] = -1*sin(ship.angle)
    rotationMatrix[1][0] = sin(ship.angle)
    rotationMatrix[1][1] = cos(ship.angle)
    
    points = rotationMatrix.dot(shipAt0)
    
    shipPoints = ((ship.x+points[0][0],ship.y+points[1][0]) , (ship.x+points[0][1],ship.y+points[1][1]) , (ship.x+points[0][2],ship.y+points[1][2]) , (ship.x+points[0][3],ship.y+points[1][3]))
    pygame.draw.polygon(displaySurf, white, shipPoints , 1) #(surface to draw to, color, coordinates, width)

    pygame.display.update()
    fpsClock.tick()
