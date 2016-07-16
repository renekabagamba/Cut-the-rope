import pygame
from gameClasses import *
from levelOne import init_LevelOne
from levelTwo import init_LevelTwo
from levelThree import init_LevelThree

black = (0,0,0)
white = (255,255,255)
orangered = (255,69,0)
blue = (0,0,255)

####################################
# init
####################################

def init_levelsMenu(data):
    data.levelsMenuObjects = []
    data.levelMenu = loadImage('background.png')
    data.buttonSizeW = 150
    data.buttonSizeL = 50
    data.buttons = 3
    data.buttonsPos = []
    data.labels = ['level 1','level 2','level 3']
    data.modeLabel = ['levelOne','levelTwo','levelThree']    
    setUp_levels_Menu(data)


def setUp_levels_Menu(data):
    data.levelMenu = pygame.transform.scale(data.levelMenu, 
                                        (data.width, data.height))

    # levels access buttons
    for i in range(data.buttons):
        (x,y,width,height) = (data.width/2-data.buttonSizeW/2,
                                     (i+1)*data.height/4-data.buttonSizeL/2,
                                     data.buttonSizeW,data.buttonSizeL)

        data.buttonsPos += [(x,y,width,height)] 



####################################
# levelsMenu mode
####################################

def levelsMenuMousePressed(event, data):
    (x,y) = pygame.mouse.get_pos()

    for i in range(len(data.buttonsPos)):
        (pos_x,pos_y,width,height) = data.buttonsPos[i]
        if ( pos_x  < x < pos_x + width  and   pos_y  < y < pos_y+height ):
            
            # initialize mode
            if i == 0: init_LevelOne(data)
            elif i == 1: init_LevelTwo(data)
            elif i == 2: init_LevelThree(data)

            #change mode
            data.mode = data.modeLabel[i]
            
    if (x > data.backButtonPos[0] and y > data.backButtonPos[1]):
        data.mode = 'mainMenu'
            

def levelsMenuKeyPressed(event,data):
    pass
def levelsMenuTimerFired(data):
    pass
def levelsMenuRedrawAll(canvas, data):

    # draw level background
    canvas.blit(data.levelMenu,(0,0))

    #Back button
    caption = data.font.render('Back',True,black)
    canvas.blit(caption,data.backButtonPos)


    for i in range(len(data.buttonsPos)):
        (x,y,width,height) = data.buttonsPos[i]
        pygame.draw.rect(canvas,orangered,data.buttonsPos[i])
        # label button
        caption = data.font.render(data.labels[i],True,black)
        canvas.blit(caption,(x+width/2-30,y+height/2-10))




