"""
Title: physicsManager File
Desc: Used to manage phisics / collision
Creation Date: 16/10/17
LastMod Date: 16/10/17
TODO:
*
"""

from objects.enums import ObjectName
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

    def computeVelocity(self, mapManager, scrollManager, deltaTime):
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

            speedY = (object.velocityY * deltaTime) / 1000
            speedX = (object.velocityX * deltaTime) / 1000

            (checkX, checkY) = self.checkCollision(mapManager, object, speedX, speedY)

            if checkX:
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

    def checkCollision(self, mapManager, obj, speedX, speedY):
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

        # Falling
        if (speedY > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (bottomRightY, bottomLeftY), False)

            if not chkY:
                checkY = False

            # Check collision with other obj
            (chkX, chkY) = self.checkObjectCollision(mapManager, obj, (bottomRightY, bottomLeftY), False, speedY)

            if not chkY:
                checkY = False

        # Jumping
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topRightY, topLeftY), False)

            if not chkY:
                checkY = False

            # Check collision with other obj
            (chkX, chkY) = self.checkObjectCollision(mapManager, obj, (topRightY, topLeftY), False, speedY)

            if not chkY:
                checkY = False

        # Right
        if (speedX > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topRightX, bottomRightX), True)
            if not chkX:
                checkX = False

            # Check collision with other obj
            (chkX, chkY) = self.checkObjectCollision(mapManager, obj, (topRightX, bottomRightX), True, speedX)

            if not chkX:
                checkX = False

        # Left
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topLeftX, bottomLeftX), True)
            if not chkX:
                checkX = False

            # Check collision with other obj
            (chkX, chkY) = self.checkObjectCollision(mapManager, obj, (topLeftX, bottomLeftX), True, speedX)

            if not chkX:
                checkX = False

        return (checkX, checkY)


    def checkObjectCollision(self, mapManager, obj, corners, isXAxis, speed):
        """
        Check if a corner collide an object
        :param mapManager:
        :param corner:
        :return: True/False
        """

        isPlayer = (obj.name == ObjectName.PLAYER)

        for corner in corners:
            for object in mapManager.objects.values():
                if object != obj:
                    rect = pygame.Rect(object.realX, object.realY, object.width, object.height)
                    if rect.collidepoint(corner):
                        if isXAxis:
                            if isPlayer:
                                object.velocityX += speed
                                object.contactFrameCounter = 0
                                object.isBeingPushed = True
                            return (False, True)
                        else:
                            return (True, False)
                    elif isPlayer:
                        object.contactFrameCounter += 1

                        if object.contactFrameCounter > 2 and object.isBeingPushed:
                            object.velocityX = 0
                            object.isBeingPushedX = False



            return (True, True)

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
                dialogList.append(mapManager.dialogs[dialog])
        return dialogList

physicsManager = PhysicsManager()