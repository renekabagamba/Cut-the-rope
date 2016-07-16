import pygame, os
from pygame.locals import *

# ----------------------------------------------------
# used Load image concept
#  borrowed from Mario Shell Defense project
#  http://sourceforge.net/projects/marioshelldefen/files/

def loadImage(name, colorkey=None):

    fullname = os.path.join("data", name)
    
    try:
        image = pygame.image.load(fullname)
    except (pygame.error, message):
        print ("Cannot load image:", name)
        raise (SystemExit, message)
        
    return image

# ----------------------------------------------------
    
def loadSoundFile( name ):

    class NoneSound:
        def play( self ): pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join( "data", name )

    try:
        sound = pygame.mixer.Sound( fullname )
    except (pygame.error, message):
        print ("Cannot load sound:", fullname)
        raise (SystemExit, message)

    return sound
	