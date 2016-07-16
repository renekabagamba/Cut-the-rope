# gameClasses.py
# Cut the Rope: Final project
# Rene Kabagamba + rkabagam + RW

import pygame
import math
from gameUtils import loadImage

black = (0,0,0)
white = (255,255,255)


class Frog(pygame.sprite.Sprite):
    nomOm = loadImage('omNom.png')

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.pulledByGravity = False
        self.image = loadImage('omNom.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def display(self,canvas):
        canvas.blit(self.image,(self.x,self.y))


class Candy(pygame.sprite.Sprite):
    candy = loadImage('candy.png')

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.pulledByGravity = True
        self.image = loadImage('candy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ropeAttached = False
        self.attachedRopes = []

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def display(self,canvas):
        canvas.blit(self.image,(self.x,self.y))


class Nail(pygame.sprite.Sprite):
    nail = loadImage('nail.png')
    
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.pulledByGravity = False
        self.image = loadImage('nail.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.isRopeAttached = False

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def display(self,canvas):
        canvas.blit(self.image,(self.x,self.y))



class Rope(object):
    
    def __init__(self, x0, y0,x1,y1):
        #super().__init__()
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.pulledByGravity = False
        self.attachedObjects = []

    def attached(self,other):
        other.ropeAttached = True

    def containsClick(self, x, y):
        # vertical line 
        if (self.x0 == self.x1 ):
            if ((self.x0 >= x-5/2 and self.x0 <= x+5/2)
                 and self.y0 <= y and self.y1 >= y):
                return True
        else:
            #check for cut with a non vertical line
            m = ((-self.y1) - (-self.y0))/(self.x1 - self.x0)
            b = (-self.y1) - m*self.x1
            if ( y >= -(m*x + b)-5/2 and y <=-(m*x + b)+5/2 ):
                return True

        return False

    def length(self):
        return ( (self.x0-self.x1)**2 + (self.y0-self.y1)**2 )**0.5

    def slopeAngle(self):
        return math.acos(abs(self.y0 - self.y1)/self.length())


    def display(self,canvas):
        pygame.draw.line(canvas,black,(self.x0, self.y0),(self.x1, self.y1))


class Star(pygame.sprite.Sprite):
    star = loadImage('star.png')

    def __init__(self):
        super().__init__()
        self.pulledByGravity = False
        self.image = loadImage('star.png')
        self.rect = self.image.get_rect()

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def display(self,canvas):
        canvas.blit(self.image,self.rect)



class Bubble(pygame.sprite.Sprite):
    bubble = loadImage('bubble.png')

    def __init__(self):
        super().__init__()
        
        
        self.pulledByGravity = False
        self.image = loadImage('bubble.png')
        self.rect = self.image.get_rect()

    def display(self,canvas):
        canvas.blit(self.image,self.rect)