"""
Title: physicsManager File
Desc: Used to manage phisics / collision
Creation Date: 16/10/17
LastMod Date: 16/10/17
TODO:
*
"""

from settings.objectSettings import ObjectName
from settings.objectSettings import objectProperties
from objects.enums import ObjectType

import settings.settings as settings

import math
import pygame

class PhysicsManager(object):
    """
    Manager all the gravity / collision part
    """
    def __init__(self):
        """
        Init default value
        """
        self.gravity = 500
        self.friction = 0.8
        self.nonBlockingTiles = ['0']

    def applyGravity(self, mapManager):
        """
        Apply gravity on all objects with scrolling handling for player
        :param mapManager:
        :param scrollManager:
        :param deltaTime:
        :return: Nothing
        """

        for object in mapManager.objects.values():
            if(object.velocityY < self.gravity):
                object.velocityY += self.gravity / 100

    def closedFromZero(self, val, ceil):
        if val < ceil and val > -ceil:
            return 0
        return val

    def applyFriction(self, mapManager):

        for object in mapManager.objects.values():
            if object.name != ObjectName.PLAYER:
                if object.velocityX != 0:
                    signe = -1 if object.velocityX > 0 else 1
                    object.velocityX = self.closedFromZero(object.velocityX + (signe * self.friction),0.2)

    def computeVelocity(self, mapManager, scrollManager, guiManager, deltaTime):
        """
        Apply gravity on all objects with scrolling handling for player
        :param mapManager:
        :param scrollManager:
        :param deltaTime:
        :return: Nothing
        """

        for object in mapManager.objects.values():
            # object.realX = object.x + mapManager.currentRect.x
            # object.realY = object.y + mapManager.currentRect.y

            if object.name == ObjectName.PLAYER:
                object.ninjaToFree = []
                object.updateEmpoweringPushingTime(deltaTime)
                object.updateDisabledTime(deltaTime)

            speedY = (object.velocityY * deltaTime) / 1000
            speedX = int((object.velocityX * deltaTime) / 1000)

            (checkX, checkY) = self.checkCollision(mapManager, object, speedX, speedY, guiManager)

            if checkX:
                if object.name == ObjectName.PLAYER:
                    scrollValue = scrollManager.isScrollNeeded(mapManager, object, speedX, speedY)

                    if scrollValue:
                        if scrollValue[0] > 0 and speedX > 0 or scrollValue[0] < 0 and speedX < 0:
                            mapManager.scrollMap(scrollValue[0], 0)

                            if checkY and object.isOnGround:
                                object.realY += speedY

                                if speedY > 0:
                                    object.isOnGround = False
                            elif not checkY:
                                object.isOnGround = True

                object.realX += speedX
            if checkY:
                if object.name == ObjectName.PLAYER:
                    scrollValue = scrollManager.isScrollNeeded(mapManager, object, speedX, speedY)

                    if scrollValue:
                        if scrollValue[1] > 0 and speedY > 0 or scrollValue[1] < 0 and speedY < 0:
                            mapManager.scrollMap(0, scrollValue[1])

                            if checkX:
                                object.realX += speedX

                object.realY += speedY

                if speedY > 0:
                    object.isOnGround = False
            else:
                if speedY > 0:
                    object.isOnGround = True
                else:
                    object.isOnGround = False
                    object.velocityY = 0

    def checkCollision(self, mapManager, obj, speedX, speedY, guiManager):
        """
        Check tile and object collision for an object
        :param mapManager:
        :param obj:
        :param distX:
        :param distY:
        :return: True/False if can move or not
        """
        # Get future position on global map

        currentX = obj.realX
        currentY = obj.realY

        newX = currentX + speedX
        newY = currentY + speedY

        topLeftX = (newX, currentY)
        topRightX = (newX + obj.width, currentY)
        bottomLeftX = (newX, currentY + obj.height)
        bottomRightX = (newX + obj.width, currentY + obj.height)

        topLeftY = (currentX, newY)
        topRightY = (currentX + obj.width, newY)
        bottomLeftY = (currentX, newY + obj.height)
        bottomRightY = (currentX + obj.width, newY + obj.height)

        checkX = True
        checkY = True

        topLeftYCollision = self.checkObjectCollision(mapManager, obj, topLeftY)
        topRightYCollision = self.checkObjectCollision(mapManager, obj, topRightY)
        bottomLeftYCollision = self.checkObjectCollision(mapManager, obj, bottomLeftY)
        bottomRightYCollision = self.checkObjectCollision(mapManager, obj, bottomRightY)
        topLeftXCollision = self.checkObjectCollision(mapManager, obj, topLeftX)
        topRightXCollision = self.checkObjectCollision(mapManager, obj, topRightX)
        bottomLeftXCollision = self.checkObjectCollision(mapManager, obj, bottomLeftX)
        bottomRightXCollision = self.checkObjectCollision(mapManager, obj, bottomRightX)

        # Falling
        if (speedY > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (bottomRightY, bottomLeftY), False)

            if not chkY and checkY:
                checkY = False

            # Check collision with other obj
            if bottomLeftYCollision or bottomRightYCollision:
                if obj.name == ObjectName.PLAYER:
                    self.checkDmgAble([bottomLeftYCollision, bottomRightYCollision],
                                          obj, guiManager)

                    self.checkNinjaAble([bottomLeftYCollision, bottomRightYCollision],
                                          obj)


                checkY = False

        # Jumping
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topRightY, topLeftY), False)

            if not chkY and checkY:
                checkY = False

            # Check collision with other obj
            if topLeftYCollision or topRightYCollision:
                if obj.name == ObjectName.PLAYER:
                    self.checkDmgAble([topLeftYCollision, topRightYCollision],
                                          obj, guiManager)

                    self.checkNinjaAble([topLeftYCollision, topRightYCollision],
                                        obj)

                checkY = False

        # Right
        if (speedX > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topRightX, bottomRightX), True)
            if not chkX and checkX:
                checkX = False

            # Check collision with other obj
            if topRightXCollision or bottomRightXCollision:
                if obj.name == ObjectName.PLAYER and obj.pushMode:
                    self.checkPushable([topRightXCollision,bottomRightXCollision],
                                       obj, speedX, guiManager)
                if obj.name == ObjectName.PLAYER:
                    self.checkDmgAble([topRightXCollision, bottomRightXCollision],
                                          obj, guiManager)

                    self.checkNinjaAble([topRightXCollision, bottomRightXCollision],
                                        obj)

                checkX = False

        # Left
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topLeftX, bottomLeftX), True)
            if not chkX and checkX:
                checkX = False

            # Check collision with other obj
            if bottomLeftXCollision or topLeftXCollision:
                if obj.name == ObjectName.PLAYER and obj.pushMode:
                    self.checkPushable([bottomLeftXCollision,topLeftXCollision],
                                       obj, speedX, guiManager)
                if obj.name == ObjectName.PLAYER:
                    self.checkDmgAble([bottomLeftXCollision, topLeftXCollision],
                                      obj, guiManager)

                    self.checkNinjaAble([bottomLeftXCollision, topLeftXCollision],
                                        obj)
                checkX = False

        return (checkX, checkY)

    def checkPushable(self, objectList, player, speedX, guiManager):
        pushFactor = 2 if player.empowerNext or player.isEmpoweredPushing else 1
        pushPower = pushFactor * player.pushPower
        for obj in objectList:
            if obj and objectProperties[obj.name]["isMovable"] and pushPower >= obj.weight:
                if player.empowerNext:
                    player.isEmpoweredPushing = True
                    player.consumeEmpower(guiManager)
                else:
                    player.isPushing = True
                obj.velocityX += speedX/3
                if obj.velocityX > settings.MAX_VELOCITY_X/3:
                    obj.velocityX = settings.MAX_VELOCITY_X

    def checkDmgAble(self, objectList, player, guiManager):
        for obj in objectList:
            if obj and obj.type == ObjectType.TRAP:
                if not player.disabled:
                    player.takeDmg(guiManager)

    def checkNinjaAble(self, objectList, player):
        for obj in objectList:
            if obj and obj.type == ObjectType.NINJA:
                if not obj.isFree and not obj in player.ninjaToFree:
                    player.ninjaToFree.append(obj)

    def checkObjectCollision(self, mapManager, obj, corner):
        """
        Check if a corner collide an object
        :param mapManager:
        :param corner:
        :return: object/None
        """

        for object in mapManager.objects.values():
            libre = object.type == ObjectType.NINJA and object.isFree
            if object != obj and not libre:
                rect = pygame.Rect(object.realX,object.realY,object.width,object.height)
                if rect.collidepoint(corner):
                    return object
        return None

    def checkTileCollision(self, mapManager, obj, corners, isXAxis):
        """
        Check tile collision of the object
        :param mapManager:
        :param obj:
        :param newX:
        :param newY:
        :return: True/False if can move or not
        """

        collision = 0

        for x, y in corners:
            tileX = math.floor(x / mapManager.tileWidth)
            tileY = math.floor(y / mapManager.tileHeight)

            if tileX >= mapManager.width or tileY >= mapManager.height or tileX < 0 or tileY < 0:
                return (False, False)

            if mapManager.tiles[tileY][tileX] not in self.nonBlockingTiles:
                if isXAxis:
                    return (False, True)
                else:
                    return (True, False)
        return (True, True)


    def checkDialogCollision(self, mapManager):
        """
        Check dialog collision must be done after moving the player
        :param self:
        :param mapManager:
        :return: list of dialog
        """
        # TODO: Maybe could use the corner in checkcollision fct but not enough time ...
        dialogList = []
        player = mapManager.objects[settings.PLAYER_ID]
        topLeft = (player.realX, player.realY)
        topRight = (player.realX + player.width, player.realY)
        bottomLeft = (player.realX, player.realY + player.height)
        bottomRight = (player.realX + player.width, player.realY + player.height)
        for x,y in [topLeft,topRight,bottomLeft,bottomRight]:
            tileX = math.floor(x / mapManager.tileWidth)
            tileY = math.floor(y / mapManager.tileHeight)
            dialog = mapManager.dialogsTile[tileY][tileX]
            if dialog not in self.nonBlockingTiles:
                if not mapManager.dialogs[dialog] in dialogList:
                    dialogList.append(mapManager.dialogs[dialog])
        return dialogList

physicsManager = PhysicsManager()