from math import *
from pygame import draw
class Laser:
    def __init__(self,shipTip = (0,0),angle = 0):
        self.yAdd = 10*sin(angle)
        self.xAdd = 10*cos(angle)
        self.points = [shipTip[0], shipTip[1], shipTip[0]+self.xAdd, shipTip[1]+self.yAdd] # tipX, tipY, tailX, tailY
        
    def draw(self, displaySurf,color):
        draw.line(displaySurf, color, (self.points[0], self.points[1]), (self.points[2], self.points[3]), 1)
        self.points[0] += self.xAdd
        self.points[1] += self.yAdd
        self.points[2] += self.xAdd
        self.points[3] += self.yAdd
