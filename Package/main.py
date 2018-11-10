from ship import Ship
from laser import Laser
from asteroid import *
from button import Button
import pygame, sys
from math import *
from pygame.locals import *

pygame.font.init()
font = pygame.font.SysFont(None,50)
scoreFont = pygame.font.SysFont(None,20)
menuFont = pygame.font.SysFont(None,25)

#variables
windowWidth = 800
windowHeight = 800
score = 0
gameOver = False
gameState = "GAME"


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
reset = Button(windowWidth/2, windowHeight/2,"Try Again?")
start = Button(windowWidth/2, windowHeight/2,"Start")
#------------GAME lOOP--------------------------
while True:
    if gameState == "MENU":
        #----------------------------------MENU-------------------------------
        title = font.render("ASTEROIDS",True,white)
        displaySurf.blit(title ,(windowWidth/2 - 75,windowHeight/4))
        '''
        if start.draw(displaySurf) == "pressed":
            gameState = "GAME"
        '''
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        displaySurf.fill(black) #blank the screen first
        pygame.display.update()



        #------------------------------END-MENU-------------------------------
    elif gameState == "GAME":
        #----------------------------------GAMEPLAY-------------------------------


        #READ KEYBOARD-------
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key==32 and gameOver == False:
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
        
        #-END-READ-KEYBOARD---
        

        if len(asteroids) < 6:
            asteroids.append(Asteroid(windowWidth, windowHeight))

        
        
        #---DRAW-------------
        displaySurf.fill(black) #blank the screen first

        if gameOver == False:
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

        if gameOver == True:
            youDead = font.render("You Dead.",True,white)
            displaySurf.blit(youDead ,(windowWidth/2 - 75,windowHeight/4))
            pressed = reset.draw(displaySurf)
            if pressed == "pressed":
                gameOver = False
                ship.x = windowWidth/2
                ship.y = windowHeight/2
                ship.xVelocity = 0
                ship.yVelocity = 0
                ship.thrust = 0
                ship.angle = 3*(pi/2)
                score = 0
                for x in range(0,len(asteroids)):
                    asteroids.pop()
            
                
            

        pygame.display.update()
            #----END-DRAW-------
    
            
    #------------------------------------END-GAMEPLAY-----------------------

