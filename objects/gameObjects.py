
import settings.settings as settings
from objects.animation import AnimatedSprite
from settings.objectSettings import ObjectsAnimations

import pygame

class GameObject:
    '''
    Base class of a game object
    '''

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.tileX = tileX
        self.tileY = tileY
        self.width = width
        self.height = height
        self.velocityY = 0
        self.velocityX = 0
        self.isOnGround = False

        self.spriteSheet = pygame.image.load(ObjectsAnimations[name]['imgPath'])
        self.animatedSprite = AnimatedSprite(
            self.spriteSheet,
            ObjectsAnimations[name]['maxSpriteW'],
            ObjectsAnimations[name]['maxSpriteH'],
            ObjectsAnimations[name]['imgRatio'],
            ObjectsAnimations[name]['imgRatio']
        )
        self.width = self.animatedSprite.imgW
        self.height = self.animatedSprite.imgH
        for animation in ObjectsAnimations[name]['animations']:
            self.animatedSprite.addAnimation(
                animation["name"],
                animation["spriteNumber"],
                animation["direction"],
                animation["line"],
                animation["isDefault"],
                animation["timeDuration"]
            )
        self.animatedSprite.changeToDefaultAnimation()

    def blit(self, screen, objectsImg):
        screen.blit(self.spriteSheet, (self.x, self.y), self.animatedSprite.currentRect)

    def moveBy(self, distX, distY):
        self.x += distX
        self.y += distY
        # TODO recalculate tileX,tileY


class Ninja(GameObject):
    """
    A Ninja
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        super(Ninja, self).__init__(name, type, x, y, tileX, tileY, width, height)

 #   def blit(self,screen,objectsImg):
 #       screen.blit(objectsImg[self.name], (self.x, self.y), self.currentRect)

    def initSpriteSheet(self):
        # NEED TO PUT THEESE VALUE SOMEWHERE ...
        self.width /= 5 # Number of positions in one line
        self.height /= 5
        self.currentRect = pygame.Rect(0,0,self.width,self.height)

class Player(GameObject):
    """
    A player
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        super(Player, self).__init__(name, type, x, y, tileX, tileY, width, height)

 #   def blit(self,screen,objectsImg):
 #       screen.blit(objectsImg[self.name], (self.x, self.y), self.currentRect)

    def initSpriteSheet(self):
        # NEED TO PUT THEESE VALUE SOMEWHERE ...
        self.width /= 5 # Number of positions in one line
        self.height /= 5
        self.currentRect = pygame.Rect(0,0,self.width,self.height)

class Trap(GameObject):
    """
    A trap
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        super(Trap, self).__init__(name, type, x, y, tileX, tileY, width, height)