# Final project.py
# Cut the Rope
# Rene Kabagamba + rkabagam + RW

import pygame
import math
from gameClasses import *
from mainMenu import *
from levelsMenu import *
from levelOne import *
from levelTwo import *
from levelThree import *
from testlevel import *
from gameUtils import loadImage

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

# splash screen code adapted from notes mode-demo.py # fall2015 week7

####################################
# init
####################################

def init(data):
    data.mode = "mainMenu"
    data.time = 0
    data.timer = 0
    data.countdown = 60
    # data.mode = 'testLevel'
    data.margin = 30
    data.gravity = 2
    data.backButtonPos = (data.width-50,data.height-20)
    data.caption = 'Cut the Rope'
    pygame.display.set_caption(data.caption)
    gameIcon = loadImage('gameIcon.png',-1) 
    pygame.display.set_icon(gameIcon)
    data.level_bg = loadImage('background.png')
    data.font = pygame.font.Font('freesansbold.ttf', 20)

    init_mainMenu(data)
    init_levelsMenu(data)
    init_LevelTest(data)


####################################
# mode dispatcher
####################################

def mousePressed(event, data):
    # print (event)
    if (data.mode == "mainMenu"): mainMenuMousePressed(event, data)
    elif(data.mode == "levelsMenu"): levelsMenuMousePressed(event, data)
    elif(data.mode == "levelOne"): levelOneMousePressed(event, data)
    elif(data.mode == "levelTwo"): levelTwoMousePressed(event, data)
    elif(data.mode == "levelThree"): levelThreeMousePressed(event, data)
    elif(data.mode == 'testLevel'): testLevelMousePressed(event,data)


def keyPressed(event,data):
    if (data.mode == "mainMenu"): mainMenuKeyPressed(event,data)
    elif(data.mode == "levelsMenu"): levelsMenuKeyPressed(event,data)
    elif(data.mode == "levelOne"): levelOneKeyPressed(event,data)     
    elif(data.mode == "levelTwo"): levelTwoKeyPressed(event,data)
    elif(data.mode == "levelThree"): levelThreeKeyPressed(event,data)
    elif(data.mode == "testLevel"): testLevelKeyPressed(event,data)



def timerFired(data):
    if (data.mode == "mainMenu"): mainMenuTimerFired(data)
    elif(data.mode == "levelsMenu"): levelsMenuTimerFired(data)
    elif(data.mode == "levelOne"): levelOneTimerFired(data) 
    elif(data.mode == "levelTwo"): levelTwoTimerFired(data)
    elif(data.mode == "levelThree"): levelThreeTimerFired(data)
    elif(data.mode == "testLevel"): testLevelTimerFired(data) 


def redrawAll(canvas, data):    
    if (data.mode == "mainMenu"): mainMenuRedrawAll(canvas, data)
    elif(data.mode == "levelsMenu"): levelsMenuRedrawAll(canvas, data)
    elif(data.mode == "levelOne"): levelOneRedrawAll(canvas, data) 
    elif(data.mode == "levelTwo"): levelTwoRedrawAll(canvas, data) 
    elif(data.mode == "levelThree"): levelThreeRedrawAll(canvas, data) 
    elif(data.mode == "testLevel"): testLevelRedrawAll(canvas, data) 


####################################
# mainMenu mode
####################################

# ------ in mainMenu.py ------------


####################################
# levelsMenu mode
####################################

# ----- in levelsMenu.py ------------

####################################
# level 1 mode
####################################

# ----- in levelOne.py ------------


####################################
# level 2 mode
####################################

# ----- in levelTwo.py ------------


####################################
# level 3 mode
####################################

# ----- in levelThree.py ------------


# --- test level -----
#    in testlevel.py




####################################
# run function 
####################################

def run(width=300, height=300):
    #initialize the imported pygame modules
    pygame.init()

    pygame.mixer.music.load('audio_main.mp3')
    pygame.mixer.music.play(-1)

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 60 # frames per second
    init(data)

    canvas = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    
    counter = 0
    # This is the Main Loop of the Game
    def mainloop():
        running = True
        while running:
            clock.tick(data.timerDelay)
            nonlocal counter
            counter += 1 
            if counter == 60:
                data.timer += 1
                data.countdown -= 1
                print(data.timer)
                counter = 0
            
            for event in pygame.event.get():
                click = pygame.mouse.get_pressed()
                if event.type == pygame.QUIT:
                    running = False
                if (click[0] == 1): 
                    mousePressed(event, data)

                 
            canvas.fill(white) # clear canvas
            redrawAll(canvas, data)
            timerFired(data) 
            pygame.display.update() # update canvas


    mainloop()
    pygame.quit()
    print("bye!")    


####################################

if __name__ == "__main__":
    run(400, 600)



