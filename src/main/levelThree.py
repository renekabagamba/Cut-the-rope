import pygame
from gameClasses import *

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

####################################
# init
####################################

def init_LevelThree(data):
    pygame.mixer.music.stop()
    pygame.mixer.music.load('audio_levels.mp3')
    pygame.mixer.music.play(-1)

    data.timer = 0
    data.countdown = 60
    data.invalidMove = False
    data.mouseDown = False
    data.nails = []
    data.ropes = []
    data.actionableNails = []
    data.actionableNailBound = 80
    data.levelThreeObjects = pygame.sprite.Group()
    data.level_bg = pygame.transform.scale(data.level_bg, 
                                        (data.width, data.height))

    setUp_Level_Three(data)


def setUp_Level_Three(data):
    # set up frog
    (sizeX_om,sizeY_om) = Frog.nomOm.get_size()
    NomOm = Frog(data.width - sizeX_om,data.height-sizeY_om-data.margin)
    data.levelThreeObjects.add(NomOm)

    #set up nails
    (sizeX_nail,sizeY_nail) = Nail.nail.get_size()
    for i in range(2):
        nail = Nail(data.margin+data.width*(i)/3 - sizeX_nail/2, 
                                        data.height/3-data.margin)
        data.nails.append(nail)
        data.levelThreeObjects.add(nail)


    # actionable nails
    for i in range(2):
        if (i == 0):
            nail = Nail(2*data.margin+data.width*(i+1)/3 - sizeX_nail/2, 
                                        data.height/3+2*data.margin)
        else:
            nail = Nail(2*data.margin+data.width*(i+1)/3 - sizeX_nail/2, 
                                        data.height/3-2*data.margin)

        (cx,cy) = (nail.rect.x + sizeX_nail/2,nail.rect.y + sizeY_nail/2)

        data.actionableNails.append(nail)

        data.levelThreeObjects.add(nail)

    # set up candy
    (sizeX_candy,sizeY_candy) = Candy.candy.get_size()
    data.candy = Candy( (data.width/3)/2 - sizeX_candy/2 + 
                        data.margin,data.height/2 - sizeY_candy/2) 
    data.levelThreeObjects.add(data.candy) 


    # set up rope
    for nail in data.nails:
        rope = Rope(nail.getX() + sizeX_nail/2,nail.getY()+sizeY_nail/2,
                data.candy.getX()+sizeX_candy/2,data.candy.getY()+
                                                            sizeY_candy/2)
        rope.attached(data.candy)
        data.candy.attachedRopes.append(rope)  
        rope.attachedObjects.append(data.candy)
        rope.attachedObjects.append(nail)
        nail.isRopeAttached = True
        data.ropes.append(rope)

    # Bubble
    bubble = Bubble()
    bubble.rect.x = data.candy.rect.x
    bubble.rect.y = data.candy.rect.y + 100
    data.levelThreeObjects.add(bubble) 



####################################
# level 3 mode
####################################

def levelThreeMousePressed(event,data):

    (x,y) = pygame.mouse.get_pos()

    data.mouseDown = True
    data.x = x
    data.y = y

    for rope in data.ropes:
         if rope.containsClick(x, y):
            if rope in data.candy.attachedRopes:
                data.candy.attachedRopes.remove(rope)
                rope.attachedObjects.remove(data.candy)
            for object in rope.attachedObjects:
                # object.ropeAttached = False
                if isinstance(object,Nail):
                    object.isRopeAttached = False


    # back button pressed
    if (x > data.backButtonPos[0] and y > data.backButtonPos[1]):
        data.mode = 'levelsMenu'
        pygame.mixer.music.stop()


def levelThreeKeyPressed(event,data):
    pass


def levelThreeTimerFired(data):

    data.invalidMove = False
    data.time += 0.5

    (candy_width,candy_height) = Candy.candy.get_size()
    
    for i in range(len(data.nails)):
        if data.nails[i].isRopeAttached:

            data.theta = data.theta_max[i] * math.sin(math.sqrt(data.gravity/
                                                data.rope_length[i])*data.time)

            # new candy position
            new_x = ((data.nails[i].rect.x + candy_width/2) -\
                                    math.sin(data.theta)*data.rope_length[i])-\
                                        candy_width/2
            new_y = abs((data.nails[i].rect.y+candy_height/2) -\
                                    math.cos(data.theta)*data.rope_length[i])+\
                                        candy_height/2

            # check that all ropes allow move and make move
            for rope in data.candy.attachedRopes:
                max_length = rope.length()
                (prev_x,prev_y) = (rope.x1,rope.y1)
                rope.x1 = new_x
                rope.y1 = new_y

                #   if not valid changes, undo
                if rope.length() > max_length:
                    rope.x1 = prev_x
                    rope.y1 = prev_y
                    data.invalidMove = True
                    break


            # if all ropes allow move, perform move
            if not data.invalidMove:

                # update candy position
                data.candy.rect.x = ((data.nails[i].rect.x + candy_width/2) -\
                                    math.sin(data.theta)*data.rope_length[i])-\
                                            candy_width/2

                data.candy.rect.y = abs((data.nails[i].rect.y+candy_height/2)-\
                                    math.cos(data.theta)*data.rope_length[i])+\
                                            candy_height/2

            # # update the rope position
            for rope in data.ropes:
                if data.candy in rope.attachedObjects:
                    rope.x1 = data.candy.rect.x + candy_width/2
                    rope.y1 = data.candy.rect.y + candy_height/2

        # check for released candy
        for object in data.levelThreeObjects:
            if ( object.pulledByGravity and len(object.attachedRopes) == 0 ):
                object.rect.y += data.gravity
                if (object.rect.y < data.height) :
                    objectRect = object.rect.move(object.rect.x,object.rect.y)



def levelThreeRedrawAll(canvas, data):

    # draw level background
    canvas.blit(data.level_bg,(0,0))

    # Timer
    font = pygame.font.Font('freesansbold.ttf', 20)
    caption = font.render('Timer: '+str(data.countdown),True,black)
    canvas.blit(caption,(10,0))

    #Back button
    caption = data.font.render('Back',True,black)
    canvas.blit(caption,data.backButtonPos)

    # mousse pressed surrounding circle
    if data.mouseDown:
        pygame.draw.circle(canvas,white,(data.x,data.y),5)

    # draw elements
    data.levelThreeObjects.draw(canvas)

    # actionable nails area
    for nail in data.actionableNails:

        center = (int(nail.rect.x + Nail.nail.get_size()[0]/2),
            int(nail.rect.y + Nail.nail.get_size()[1]/2))

        pygame.draw.circle(canvas,black,center,data.actionableNailBound, 2)
        
        # if actionable nail still not used 
        if not nail.isRopeAttached:
        # if candy in range of actionable nail, draw rope
            if (data.candy.rect.x - center[0])**2 +\
            (data.candy.rect.x - center[1])**2 ==(data.actionableNailBound)**2:

                rope = Rope(center[0],center[1],
                    data.candy.getX()+sizeX_candy/2,data.candy.getY()+
                                                        sizeY_candy/2)
                # set up rope
                rope.attached(data.candy)
                data.candy.attachedRopes.append(rope)  
                rope.attachedObjects.append(data.candy)
                rope.attachedObjects.append(nail)
                nail.isRopeAttached = True
                data.ropes.append(rope)

    # draw ropes
    for rope in data.ropes:
        rope.display(canvas)



    


