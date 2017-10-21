"""
Title: physicsManager File
Desc: Used to manage phisics / collision
Creation Date: 16/10/17
LastMod Date: 16/10/17
TODO:
*
"""

from objects.enums import ObjectName

import math

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

            if object.name == ObjectName.PLAYER:
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

            if not chkY and checkY:
                checkY = False

        # Jumping
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topRightY, topLeftY), False)

            if not chkY and checkY:
                checkY = False

        # Right
        if (speedX > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topRightX, bottomRightX), True)
            if not chkX and checkX:
                checkX = False

        # Left
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topLeftX, bottomLeftX), True)
            if not chkX and checkX:
                checkX = False

        return (checkX, checkY)

        # Check collision with other obj
        # SOON

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
                print("out")
                return (False, False)

            if mapManager.tiles[tileY][tileX] not in self.nonBlockingTiles:
                if isXAxis:
                    return (False, True)
                else:
                    return (True, False)

        return (True, True)

physicsManager = PhysicsManager()