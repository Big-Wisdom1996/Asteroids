from ship import Ship
from laser import Laser
from asteroid import *
import pygame, sys
from math import *
from pygame.locals import *

pygame.font.init()
font = pygame.font.SysFont(None,50)
scoreFont = pygame.font.SysFont(None,20)
def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    displaySurf.blit(screen_text,(windowWidth/2,windowHeight/2))

#variables
windowWidth = 800
windowHeight = 800
score = 0
gameOver = False


#set up window
pygame.init()
displaySurf = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption('Asteroids')



#colors
white = (255,255,255)
black = (0 , 0 , 0)

#OBJECTS
ship = Ship(white,windowWidth,windowHeight)
asteroids = []
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

    if len(asteroids) < 3:
        asteroids.append(Asteroid(windowWidth, windowHeight))

    if not gameOver: 
        #---DRAW-------------
        displaySurf.fill(black) #blank the screen first
        ship.draw(displaySurf,windowWidth,windowHeight,white)
        for laser in lasers:
            laser.draw(displaySurf, white)
            # remove laser object if it leaves the screen
            if laser.points[2] > windowWidth or laser.points[2] < 0 or laser.points[3] > windowHeight or laser.points[3] < 0:
                lasers.remove(laser)

        for asteroid in asteroids:
            asteroid.draw(displaySurf, white, windowWidth, windowHeight)

            laserHit = asteroid.checkLasers(lasers)
            if laserHit != None:
                lasers.remove(laserHit)
                asteroids.remove(asteroid)
                
                if asteroid.shape == 1:
                    asteroids.append(SmallAsteroid(asteroid.x, asteroid.y, asteroid.xVelocity, asteroid.yVelocity, "left"))
                    asteroids.append(SmallAsteroid(asteroid.x, asteroid.y, asteroid.xVelocity, asteroid.yVelocity, "right"))
                    score += 10
                elif(asteroid.shape == 2):
                    score += 20

            asteroidHit = ship.check(asteroid)
            if asteroidHit != None:
                asteroids.remove(asteroidHit)
                gameOver = True
                

        screen_text = scoreFont.render("Score: "+str(score), True, white)
        displaySurf.blit(screen_text,(windowWidth - 100,40))

            
        
        #--------------------
    else:
        message_to_screen("You Dead.",white)
    
    
    pygame.display.update()
#-----------------------------------------------

