

import pygame
from gameUtils import loadImage

white = (255,255,255)

class Candy(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.pulledByGravity = True
        self.image = loadImage('candy.png')
        self.rect = self.image.get_rect()
        self.ropeAttached = False

    def getX(self):
        return self.rect.x
    def getY(self):
        return self.rect.y


    def display(self,canvas):
        canvas.blit(self.object,self.rect)

class Star(pygame.sprite.Sprite):
    star = loadImage('star.png')

    def __init__(self):
        super().__init__()
        self.pulledByGravity = False
        self.image = loadImage('star.png')
        self.rect = self.image.get_rect()

    # def getX(self):
    #     return self.x
    # def getY(self):
    #     return self.y

    def display(self,canvas):
        canvas.blit(self.image,self.rect)


def init(data):
    data.candy = Candy()
    data.sprite_list = pygame.sprite.Group()
    data.sprite_list.add(data.candy)
    data.star = Star()
    data.sprite_list.add(data.star)
    data.star.rect.x = 200
    data.star.rect.y = 200

def mousePressed(event, data):
    pass

def keyPressed(event,data):
    pass


def timerFired(data):
    data.candy.rect.x += 2
    data.candy.rect.y += 2    


def redrawAll(canvas, data):
    data.sprite_list.remove(data.candy)
    pygame.sprite.spritecollide(data.candy,data.sprite_list,True)
    data.sprite_list.add(data.candy)

    data.sprite_list.draw(canvas)




def run(width=300, height=300):
    #initialize the imported pygame modules
    pygame.init()

    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 60 # frames per second
    init(data)

    canvas = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    

    # This is the Main Loop of the Game
    def mainloop():
        running = True
        while running:
            clock.tick(data.timerDelay)
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