from ship import Ship
from laser import Laser
import pygame, sys
from math import *
from pygame.locals import *

#set up window
pygame.init()
windowWidth = 800
windowHeight = 800
displaySurf = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption('Asteroids')

#colors
white = (255,255,255)
black = (0 , 0 , 0)

#OBJECTS
ship = Ship(white,windowWidth,windowHeight)
lasers = []
#------------GAME lOOP--------------------------
while True:
    #READ KEYBOARD-------
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key==32:
                lasers.append(Laser(ship.shipPoints[0],ship.angle))
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
    #---------------------


    #---DRAW-------------
    displaySurf.fill(black) #blank the screen first
    ship.draw(displaySurf,windowWidth,windowHeight,white)
    for laser in lasers:
        laser.draw(displaySurf, white)
        # remove laser object if it leaves the screen
        if laser.points[2] > windowWidth or laser.points[2] < 0 or laser.points[3] > windowHeight or laser.points[3] < 0:
            lasers.remove(laser)
            print(lasers)
    #--------------------

    
    pygame.display.update()
#-----------------------------------------------

