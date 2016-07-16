import pygame
from gameClasses import *

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

####################################
# init
####################################

def init_LevelTest(data):
    data.score = 0
    data.starsCount = 1
    data.stars = pygame.sprite.Group()
    data.starsCollected = []
    data.testLevelObjects = pygame.sprite.Group()
    data.nails = []
    data.ropes = []
    data.level_bg = pygame.transform.scale(data.level_bg, 
                                        (data.width, data.height))

    setUp_Level_test(data)

def setUp_Level_test(data):
    # set up frog
    (sizeX_om,sizeY_om) = Frog.nomOm.get_size()
    NomOm = Frog(data.width/2-sizeX_om/2,data.height-sizeY_om)
    data.testLevelObjects.add(NomOm)

    #set up nails
    (sizeX_nail,sizeY_nail) = Nail.nail.get_size()
    for i in range(1):
        nail = Nail(data.margin+data.width*(i+1)/3 - sizeX_nail/2, data.margin)
        data.nails.append(nail)
        data.testLevelObjects.add(nail)

    # set up candy
    (sizeX_candy,sizeY_candy) = Candy.candy.get_size()
    data.candy = Candy(data.margin - sizeX_candy/2,data.height/3 - 
                                                        sizeY_candy/2) 
    data.testLevelObjects.add(data.candy) 

    # set up rope
    for nail in data.nails:

        rope = Rope(nail.getX() + sizeX_nail/2,nail.getY()+sizeY_nail/2,
                data.candy.getX()+sizeX_candy/2,data.candy.getY()+
                                                            sizeY_candy/2)
        rope.attached(data.candy)  
        rope.attachedObjects.append(data.candy)
        data.ropes.append(rope)

    # set up stars
    (sizeX_star,sizeY_star) = Star.star.get_size()
    for i in range(1,data.starsCount+1):
        star = Star()
        if (i == 1):
            star.rect.y = data.candy.rect.y + (i)*data.margin
            star.rect.x = data.width/2 
        # elif (i == 2):
        #     star.rect.y = data.candy.rect.y + (i+1)*data.margin
        #     star.rect.x = data.width - i*data.margin
        # else:
        #     star.rect.y = data.candy.rect.y + (i+3)*data.margin
        #     star.rect.x = data.candy.rect.x 


        data.stars.add(star)
        data.testLevelObjects.add(star)

    #theta max

    for rope in data.ropes:
        data.rope_length = rope.length()
        data.theta_max = rope.slopeAngle()




####################################
# test level mode
####################################

def testLevelMousePressed(event, data):
    pass
def testLevelKeyPressed(event,data):
    pass

def testLevelTimerFired(data):

    data.time += 0.5
    data.theta = data.theta_max * math.sin(math.sqrt(data.gravity/
                                                data.rope_length)*data.time)  

    (candy_width,candy_height) = Candy.candy.get_size()

    # update candy position
    data.candy.rect.x = ((data.nails[0].rect.x + candy_width/2) -\
                                math.sin(data.theta)*data.rope_length) -\
                                candy_width/2

    data.candy.rect.y = abs((data.nails[0].rect.y+candy_height/2) -\
                                math.cos(data.theta)*data.rope_length)+\
                                candy_height/2

    for rope in data.ropes:
        rope.x1 = data.candy.rect.x + candy_width/2
        rope.y1 = data.candy.rect.y + candy_height/2

    


def testLevelRedrawAll(canvas, data):
    
    # draw level background
    canvas.blit(data.level_bg,(0,0))

    # draw elements
    data.testLevelObjects.draw(canvas)

    # draw ropes
    for rope in data.ropes:
        rope.display(canvas)

