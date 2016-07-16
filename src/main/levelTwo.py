import pygame
from gameClasses import *

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

####################################
# init
####################################

def init_LevelTwo(data):
    pygame.mixer.music.stop()
    pygame.mixer.music.load('audio_levels.mp3')
    pygame.mixer.music.play(-1)
    
    data.rope_length = []
    data.theta_max = []
    data.score = 0
    data.mouseDown = False
    data.x = 0
    data.y = 0
    data.invalidMove = False
    data.starsCount = 3
    data.nailsCount = 2
    data.stars = pygame.sprite.Group()
    data.starsCollected = []
    data.levelTwoObjects = pygame.sprite.Group()
    data.nails = []
    data.ropes = []
    data.level_bg = pygame.transform.scale(data.level_bg, 
                                        (data.width, data.height))

    setUp_Level_Two(data)

def setUp_Level_Two(data):
    # set up frog
    (sizeX_om,sizeY_om) = Frog.nomOm.get_size()
    NomOm = Frog(data.width/2-sizeX_om/2,data.height-sizeY_om)
    data.levelTwoObjects.add(NomOm)

    #set up nails
    (sizeX_nail,sizeY_nail) = Nail.nail.get_size()
    for i in range(data.nailsCount):
        nail = Nail(data.margin+data.width*(i)/3 - sizeX_nail/2, data.margin)
        data.nails.append(nail)
        data.levelTwoObjects.add(nail)

    # set up candy
    (sizeX_candy,sizeY_candy) = Candy.candy.get_size()
    data.candy = Candy(data.margin - sizeX_candy/2,data.height/3 - 
                                                        sizeY_candy/2) 
    data.levelTwoObjects.add(data.candy) 

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

    # set up stars
    (sizeX_star,sizeY_star) = Star.star.get_size()
    for i in range(1,data.starsCount+1):
        star = Star()
        if (i == 1):
            star.rect.y = data.candy.rect.y + (i+1)*data.margin
            star.rect.x = data.candy.rect.x 
        elif (i == 2):
            star.rect.y = data.candy.rect.y + (i)*data.margin
            star.rect.x = data.width - i*data.margin
        else:
            star.rect.y = data.candy.rect.y + (i+2)*data.margin
            star.rect.x = data.candy.rect.x 


        data.stars.add(star)
        data.levelTwoObjects.add(star)

    # theta_max
    for rope in data.ropes:
        data.rope_length.append( rope.length() )
        data.theta_max.append( rope.slopeAngle() )



####################################
# level 2 mode
####################################

def levelTwoMousePressed(event, data):
    
    (x,y) = pygame.mouse.get_pos()

    data.mouseDown = True
    data.x = x
    data.y = y

    # check for rope cut
    for rope in data.ropes:
        # m = (-rope.y1 + rope.y0)/(rope.x1 - rope.x0)
        # b = -rope.y1 - m*rope.x1
        # print('rope slope: ',m)
        # print('b value: ',b)
        # print ("mouse pressed at: ",x,y)
        # expected = -(m*x+b)
        # print('x into eq: ',expected)
        if rope.containsClick(x, y):
            if rope in data.candy.attachedRopes:
                data.candy.attachedRopes.remove(rope)
                rope.attachedObjects.remove(data.candy)
            for object in rope.attachedObjects:
                # object.ropeAttached = False
                if isinstance(object,Nail):
                    object.isRopeAttached = False

                # if isinstance(object,Candy):
                #     object.attachedRopes.remove(rope)
                #     print (object.attachedRopes)


    # back button pressed
    if (x > data.backButtonPos[0] and y > data.backButtonPos[1]):
        data.mode = 'levelsMenu'
        pygame.mixer.music.stop()

def levelTwoKeyPressed(event,data):
    pass

def levelTwoTimerFired(data):
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
        for object in data.levelTwoObjects:
            if ( object.pulledByGravity and len(object.attachedRopes) == 0 ):
                object.rect.y += data.gravity
                if (object.rect.y < data.height) :
                    objectRect = object.rect.move(object.rect.x,object.rect.y)



def levelTwoRedrawAll(canvas, data):
    
    # draw level background
    canvas.blit(data.level_bg,(0,0))

    #Back button
    caption = data.font.render('Back',True,black)
    canvas.blit(caption,data.backButtonPos)

    # draw elements
    data.levelTwoObjects.draw(canvas)

    # mousse pressed surrounding circle
    if data.mouseDown:
        pygame.draw.circle(canvas,white,(data.x,data.y),5)

    # draw ropes
    for rope in data.ropes:
        rope.display(canvas)
