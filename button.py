from pygame import *

class Button:
    def __init__(self,centerX, centerY, text):
        self.centerX = int(centerX)
        self.centerY = int(centerY)
        self.corner = (self.centerX-100, self.centerY-25, 200, 50)
        self.text = text
        self.hit = False
        self.font = font.SysFont(None,25)

    def draw(self, displaySurf):
        mousePos = mouse.get_pos()
        if mousePos[0] < self.centerX + 100 and mousePos[0] > self.centerX - 100 and mousePos[1] > self.centerY - 25 and mousePos[1] < self.centerY + 25:
            draw.rect(displaySurf, (255,255,255), self.corner, 0)
            text = self.font.render(self.text,True, (0,0,0))
            displaySurf.blit(text,(self.centerX - 40,self.centerY - 10))
            if mouse.get_pressed()[0] == 1:
                return "pressed"
            else:
                return "unpressed"
        else:
            draw.rect(displaySurf, (255,255,255), self.corner, 1)
            text = self.font.render(self.text,True, (255,255,255))
            displaySurf.blit(text,(self.centerX - 40,self.centerY - 10))
            return "unpressed"

            
