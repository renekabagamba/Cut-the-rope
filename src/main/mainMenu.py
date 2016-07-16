import pygame
from gameClasses import *
from gameUtils import loadImage

black = (0,0,0)
white = (255,255,255)
orangered = (255,69,0)

####################################
# init
####################################

def init_mainMenu(data):

    data.candyLocation = None
    data.mainMenuObjects = []
    data.mainMenu_title = loadImage('main_menu_2.png')
    data.mainMenu = loadImage('background.png')
    data.mainMenu = pygame.transform.scale(data.mainMenu, 
                                        (data.width, data.height))
    setUp_main_Menu(data)

def setUp_main_Menu(data):
    #set up text
    font = pygame.font.Font(None, 36)
    # set up frog
    (sizeX_om,sizeY_om) = Frog.nomOm.get_size()
    NomOm = Frog(data.width-sizeX_om - data.margin,
                            data.height-sizeY_om - data.margin)
    data.mainMenuObjects.append(NomOm)


####################################
# mainMenu mode
####################################

def mainMenuMousePressed(event, data):
    (x,y) = pygame.mouse.get_pos()
    if  (240+78 > x > 78  and 330+52 > y > 330):
        data.mode = "levelsMenu"


def mainMenuKeyPressed(event,data):
    pass

def mainMenuTimerFired(data):
    pass

def mainMenuRedrawAll(canvas, data):

    canvas.blit(data.mainMenu,(0,0))
    canvas.blit(data.mainMenu_title,(0,0))
    
    # start Button
    pygame.draw.rect(canvas,orangered,(78,330,240,52))
    font = pygame.font.Font('freesansbold.ttf', 20)
    caption = font.render('START',True,black)
    canvas.blit(caption,(168,348))
    
    for object in reversed(data.mainMenuObjects):
        object.display(canvas)