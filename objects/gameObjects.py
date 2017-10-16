
import os
import settings.settings as settings
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

    def blit(self,screen,objectsImg):
        screen.blit(objectsImg[self.name], (self.x, self.y))

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

    def blit(self,screen,objectsImg):
        screen.blit(objectsImg[self.name], (self.x, self.y), self.currentRect)

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

    def blit(self,screen,objectsImg):
        screen.blit(objectsImg[self.name], (self.x, self.y), self.currentRect)

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