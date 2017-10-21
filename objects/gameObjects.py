
import settings.settings as settings
from objects.animation import AnimatedSprite
from settings.objectSettings import ObjectsAnimations

import pygame
import sys

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
        self.realX = x
        self.realY = y
        self.tileX = tileX
        self.tileY = tileY
        self.width = width
        self.height = height
        self.velocityY = 0
        self.velocityX = 0
        self.isOnGround = False
        self.isBeingPushed = False
        self.contactFrameCounter = 0

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

    def blit(self, mapManager, screen):
        if self.realX >= mapManager.currentRect.x - mapManager.tileWidth \
            and self.realX < mapManager.currentRect.x + mapManager.currentRect.w + mapManager.tileWidth\
            and self.realY >= mapManager.currentRect.y - mapManager.tileHeight \
            and self.realY < mapManager.currentRect.x + mapManager.currentRect.h + mapManager.tileHeight :

            self.x = self.realX - mapManager.currentRect.x
            self.y = self.realY - mapManager.currentRect.y

            screen.blit(self.animatedSprite.spriteSheet, (self.x, self.y), self.animatedSprite.currentRect)

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

        self.isFree = False

    def setFree(self):
        self.isFree = True

    def blit(self, mapManager, screen):
        if not self.isFree:
            super(Ninja, self).blit(mapManager, screen)


class Player(GameObject):
    """
    A player
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        super(Player, self).__init__(name, type, x, y, tileX, tileY, width, height)
        self.empowerNext = False
        self.pushMode = False
        self.pushPower = 100
        self.isPushing = False
        self.isEmpoweredPushing = False
        self.maxEmpoweringPushingTime = 2000
        self.currentEmpoweringPushingTime = 0

        self.disabled = False
        self.maxDisabledTime = 500
        self.currentDisabledTime = 0
        self.ninjaToFree = []

    def updateEmpoweringPushingTime(self, deltaTime):
        if self.isEmpoweredPushing:
            self.currentEmpoweringPushingTime += deltaTime
            if self.currentEmpoweringPushingTime > self.maxEmpoweringPushingTime:
                self.currentEmpoweringPushingTime = 0
                self.isEmpoweredPushing = False

    def updateDisabledTime(self, deltaTime):
        if self.disabled:
            self.currentDisabledTime += deltaTime
            if self.currentDisabledTime > self.maxDisabledTime:
                self.currentDisabledTime = 0
                self.disabled = False

    def enablePushMode(self):
        self.pushMode = True

    def disablePushMode(self):
        self.pushMode = False
        self.isPushing = False
        self.isEmpoweredPushing = False
        self.currentEmpoweringPushingTime = 0

    def empowerNextSpell(self, guiManager):
        """
        Try to empower the next spell
        :param guiManager:
        :return:
        """
        if not self.empowerNext:
            self.empowerNext = guiManager.empowerSpell()

    def consumeEmpower(self, guiManager):
        """
        Consume the empower for the spell
        :param guiManager:
        :return: Nothing
        """
        self.empowerNext = False
        guiManager.consumeWaitingEmpowering()

    def takeDmg(self, guiManager):
        self.disabled = True
        guiManager.looseLife()
        self.currentDisabledTime = 0
        signe = -1 if self.velocityX > 0 else 1
        self.velocityX = signe * (settings.MAX_VELOCITY_X/2.5)
        signe = -1 if self.velocityY > 0 else 1
        self.velocityY = signe * (settings.MAX_VELOCITY_Y/2.5)

    def freeNinjas(self, guiManager):
        for ninja in self.ninjaToFree:
            ninja.setFree()
            guiManager.addNinjaBar()

    def blit(self, mapManager, screen):
        if self.realX >= mapManager.currentRect.x - mapManager.tileWidth \
            and self.realX < mapManager.currentRect.x + mapManager.currentRect.w + mapManager.tileWidth\
            and self.realY >= mapManager.currentRect.y - mapManager.tileHeight \
            and self.realY < mapManager.currentRect.x + mapManager.currentRect.h + mapManager.tileHeight :

            self.x = self.realX - mapManager.currentRect.x
            self.y = self.realY - mapManager.currentRect.y
            if not self.disabled or ((self.currentDisabledTime // 50) % 2) == 0:
                screen.blit(self.animatedSprite.spriteSheet, (self.x, self.y), self.animatedSprite.currentRect)

class Trap(GameObject):
    """
    A trap
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        super(Trap, self).__init__(name, type, x, y, tileX, tileY, width, height)

class Box(GameObject):
    """
    A trap
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height, weight):
        '''
        Constructor

        '''

        super(Box, self).__init__(name, type, x, y, tileX, tileY, width, height)
        self.weight = weight