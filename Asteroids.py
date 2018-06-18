import pygame , sys, numpy, random
from math import *
from pygame.locals import *

pygame.init()
windowWidth = 800
windowHeight = 800
displaySurf = pygame.display.set_mode((windowWidth,windowHeight))
pygame.display.set_caption('Asteroids')
fpsClock = pygame.time.Clock()
pygame.font.init()
FPS = 5 # set frame rate to 5 per second
black = (0 , 0 , 0)
white = (255, 255, 255)
idk = (255,255,0)
impactDistance = 40
gameOver = False
#Initialize game state ----------------------------------------

class Ship():
    def __init__(self):
        self.x = windowWidth/2 # meters
        self.y = windowHeight/2 # meters
        self.mass = 100 #kg
        self.xVelocity = 0 # meters per second
        self.yVelocity = 0 # meters per second
        self.thrust = 0 # newtons
        self.angle = 3*(pi/2) # radians
        #points relative to center of ship, while ship is at angle: 0
        self.shipAt0 = numpy.array([     #Points of the ship when it's facing straight east (zero degrees)
            [25,-25,-15,-25,-20,-35,-20],
            [0,14,0,-14,7,0,-7]])
        self.rotationMatrix = numpy.array([
            [cos(self.angle),-1*sin(self.angle)],
            [sin(self.angle),cos(self.angle)]])
        self.points = 0
        self.shipPoints = 0 
        self.flamePoints = 0
        self.color = white
        

    def draw(self):
         #SHIP
        #move ship center
        ship.xVelocity += ship.thrust*cos(ship.angle)/(ship.mass) # calculate X velocity
        ship.yVelocity += ship.thrust*sin(ship.angle)/(ship.mass) # add on the acceleration ( a = f/m)
        ship.x = (ship.x+ship.xVelocity) % windowWidth
        ship.y = (ship.y+ship.yVelocity) % windowHeight

        #calculate new points
        self.rotationMatrix[0][0] = cos(self.angle)
        self.rotationMatrix[0][1] = -1*sin(self.angle)
        self.rotationMatrix[1][0] = sin(self.angle)
        self.rotationMatrix[1][1] = cos(self.angle)
    
        self.points = self.rotationMatrix.dot(self.shipAt0)
        self.shipPoints = ((self.x+self.points[0][0],self.y+self.points[1][0]) , (self.x+self.points[0][1],self.y+self.points[1][1]) , (self.x+self.points[0][2],self.y+self.points[1][2]) , (self.x+self.points[0][3],self.y+self.points[1][3]))
        self.flamePoints = ((self.x+self.points[0][4],self.y+self.points[1][4]),(self.x+self.points[0][5],self.y+self.points[1][5]),(self.x+self.points[0][6],self.y+self.points[1][6]))    
    
        pygame.draw.polygon(displaySurf, self.color, self.shipPoints , 1) #(surface to draw to, color, coordinates, width)
        if keys[pygame.K_w] == 1:
            pygame.draw.lines(displaySurf, white,(0,0), self.flamePoints, 1) 

    def check(self, asteroid):
        distance = sqrt((asteroid.x - self.x)**2+(asteroid.y-self.y)**2)
        if distance < impactDistance:
            return True
        else:
            return False
        
class Asteroid():
    def __init__(self):
        self.x = random.randint(0,windowWidth)
        self.y = random.randint(0,windowHeight)
        self.xVelocity = random.randint(-5,5)
        self.yVelocity = random.randint(-5,5)
        self.asteroidTemplate = [     
            [30,30,0,-30,-10,10],
            [2,24,40,10,-45,-45]]
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

font = pygame.font.SysFont(None,50)
def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    displaySurf.blit(screen_text,(windowWidth/2,windowHeight/2))

ship = Ship()
a1 = Asteroid()
a2 = Asteroid()
a3 = Asteroid()




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

   
 
    #draw game -----------------------------------------------
    if not gameOver:
        displaySurf.fill(black) #blank the screen first
        ship.draw()
        a1.draw() 
        a2.draw()
        a3.draw()
    else:
        message_to_screen("You Dead.",white)
    if ship.check(a1) or ship.check(a2) or ship.check(a3):
        ship.color = idk
        gameOver = True
    pygame.display.update()
    fpsClock.tick()
