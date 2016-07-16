import pygame
from gameClasses import *
from levelTwo import *

black = (0,0,0)
white = (255,255,255)
orangered = (255,69,0)

####################################
# init
####################################


def init_LevelOne(data):
    pygame.mixer.music.stop()
    pygame.mixer.music.load('audio_levels.mp3')
    pygame.mixer.music.play(-1)
    data.timer = 0
    data.score = 0
    data.end = 10
    data.buttons = 2
    data.buttonSizeW = 150
    data.buttonSizeL = 50
    data.labels1 = ['Replay','Next level']
    data.buttonsPos1 = []
    data.starsCount = 3
    data.mouseDown = False
    data.x = 0
    data.y = 0
    data.game_over = False
    data.stars = pygame.sprite.Group()
    data.ropes = []
    data.levelOneObjects = pygame.sprite.Group()
    data.starsCollected = []
    data.level_bg = pygame.transform.scale(data.level_bg, 
                                        (data.width, data.height))
    setUp_Level_One(data)


def setUp_Level_One(data):
    # set up frog
    (sizeX_om,sizeY_om) = Frog.nomOm.get_size()
    NomOm = Frog(data.width/2-sizeX_om/2,data.height-sizeY_om)
    data.levelOneObjects.add(NomOm)

    # set up nail
    (sizeX_nail,sizeY_nail) = Nail.nail.get_size()
    nail = Nail(data.width/2 - sizeX_nail/2, data.margin)
    data.levelOneObjects.add(nail)

    # set up candy
    (sizeX_candy,sizeY_candy) = Candy.candy.get_size()
    data.candy = Candy(data.width/2 - sizeX_candy/2,data.height/3 - 
                                                        sizeY_candy/2)
    data.levelOneObjects.add(data.candy)

    # set up rope 
    rope = Rope(nail.getX() + sizeX_nail/2,nail.getY()+sizeY_nail/2,
                data.candy.getX()+sizeX_candy/2,data.candy.getY()+
                                                            sizeY_candy/2)
    rope.attached(data.candy) # attached object
    rope.attachedObjects.append(data.candy) #add object to the list of attached 
    data.ropes.append(rope)             # objects

    # set up stars
    (sizeX_star,sizeY_star) = Star.star.get_size()
    for i in range(1,data.starsCount+1):
        star = Star()
        star.rect.x = data.width/2 - sizeX_star/2
        star.rect.y = data.height/3 + sizeY_candy/2 + i*sizeY_star +\
                                                     i*data.margin
        data.stars.add(star)
        data.levelOneObjects.add(star)

    print("button len in init: ",data.buttons)
    # end level buttons
    for i in range(data.buttons):
        (x,y,width,height) = ((i+1)*data.width/4-data.buttonSizeW/2+
                                    3*i*data.margin,
                                     data.height*2/3-data.buttonSizeL/2,
                                     data.buttonSizeW,data.buttonSizeL)

        data.buttonsPos1 += [(x,y,width,height)] 
    print('loaded buttons: ',data.buttonsPos1)


####################################
# level 1 mode
####################################

def levelOneMousePressed(event,data):
    (x,y) = pygame.mouse.get_pos()

    if data.game_over: 
        for i in range(len(data.buttonsPos1)):
            (pos_x,pos_y,width,height) = data.buttonsPos1[i]

            if ( pos_x  < x < pos_x + width and pos_y  < y < pos_y+height ):
                # initialize mode
                if i == 0: 
                   init_LevelOne(data) 
                elif i == 1: 
                    init_LevelTwo(data)
                    data.mode = 'levelTwo'



    data.mouseDown = True
    data.x = x
    data.y = y

    for rope in data.ropes:
        if rope.containsClick(x, y):
            for object in rope.attachedObjects:
                object.ropeAttached = False

    # back button pressed
    if (x > data.backButtonPos[0] and y > data.backButtonPos[1]):
        data.mode = 'levelsMenu'
        pygame.mixer.music.stop()



def levelOneKeyPressed(event,data):
    pass


def levelOneTimerFired(data):

    # check for collected stars
    data.starsCollected = pygame.sprite.spritecollide(data.candy,
                                                    data.stars,True)

    if not data.game_over:
        #frog eat candy
        data.levelOneObjects.remove(data.candy)

        if pygame.sprite.spritecollide(data.candy,data.levelOneObjects,False):
            data.end -= 1
            
            print(data.end)
            if (data.end <= 0):
                data.game_over = True
            else:
                data.levelOneObjects.add(data.candy)

        else:
            data.levelOneObjects.add(data.candy)
        
    # check for released candy
    for object in data.levelOneObjects:
        if (object.pulledByGravity and not object.ropeAttached) :
            object.rect.y += data.gravity
            if (object.rect.y < data.height) :
                objectRect = object.rect.move(object.rect.x,object.rect.y)

    #check collected stars
    for star in data.starsCollected:
        data.score+=1
        print(data.score,"stars collected")

            
def levelOneRedrawAll(canvas, data):

    # draw level background
    canvas.blit(data.level_bg,(0,0))

    #Back button
    caption = data.font.render('Back',True,black)
    canvas.blit(caption,data.backButtonPos)

    if not data.game_over:
        # displayed text on top
        font = pygame.font.Font('freesansbold.ttf', 20)
        caption = font.render('Click on the rope to release the candy',
                                                    True,black)
        canvas.blit(caption,(10,0))

        # caption = font.render('Timer: '+str(data.timer),True,black)
        # canvas.blit(caption,(10,20))

        # draw elements
        data.levelOneObjects.draw(canvas)

        # mousse pressed surrounding circle
        if data.mouseDown:
            pygame.draw.circle(canvas,white,(data.x,data.y),5)
            # data.mouseDown = False

        # draw ropes
        for rope in data.ropes:
            rope.display(canvas)

    # when game over
    else:
        font = pygame.font.Font('freesansbold.ttf', 20)
        caption = font.render('Level completed',True,black)
        canvas.blit(caption,(data.width/2 - 65,data.height/3))
        caption = font.render(str(data.score)+' out of 3 : stars collected',
                                                                    True,black)
        canvas.blit(caption,(data.width/2 - 100,data.height/2))

        for i in range(len(data.buttonsPos1)):
            (x,y,width,height) = data.buttonsPos1[i]
            pygame.draw.rect(canvas,orangered,data.buttonsPos1[i])
            # label button
            caption = data.font.render(data.labels1[i],True,black)
            canvas.blit(caption,(x+width/2-40,y+height/2-10))
