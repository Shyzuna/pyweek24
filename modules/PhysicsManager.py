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
            print("Gravity", object.velocityY)

    def computeVelocity(self, mapManager, scrollManager, deltaTime):
        """
        Apply gravity on all objects with scrolling handling for player
        :param mapManager:
        :param scrollManager:
        :param deltaTime:
        :return: Nothing
        """

        for object in mapManager.objects.values():
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
                                object.y += speedY

                                if speedY > 0:
                                    object.isOnGround = False
                            elif not checkY:
                                object.isOnGround = True
                        else:
                            object.x += speedX
                    else:
                        object.x += speedX
                if checkY:
                    scrollValue = scrollManager.isScrollNeeded(mapManager, object, speedX, speedY)

                    if scrollValue:
                        if scrollValue[1] > 0 and speedY > 0 or scrollValue[1] < 0 and speedY < 0:
                            mapManager.scrollMap(0, scrollValue[1])
                            if checkX:
                                object.x += speedX
                        else:
                            object.y += speedY

                            if speedY > 0:
                                object.isOnGround = False
                    else:
                        object.y += speedY

                        if speedY > 0:
                            object.isOnGround = False
                else:
                    object.isOnGround = True

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

        currentX = obj.x + mapManager.currentRect.x
        currentY = obj.y + mapManager.currentRect.y

        newX = obj.x + speedX + mapManager.currentRect.x
        newY = obj.y + speedY + mapManager.currentRect.y

        marge = 10

        topLeftX = (newX + marge, currentY + marge)
        topRightX = (newX + obj.width - marge, currentY + marge)
        bottomLeftX = (newX + marge, currentY + obj.height - marge)
        bottomRightX = (newX + obj.width - marge, currentY + obj.height - marge)

        topLeftY = (currentX + marge, newY + marge)
        topRightY = (currentX + obj.width - marge, newY + marge)
        bottomLeftY = (currentX + marge, newY + obj.height - marge)
        bottomRightY = (currentX + obj.width - marge, newY + obj.height - marge)

        checkX = True
        checkY = True

        # Two axes
        isTwoAxis = speedY != 0 and speedX != 0

        # Falling
        if (speedY > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (bottomRightY, bottomLeftY), obj.x , newY, False, isTwoAxis)

            if not chkY and checkY:
                checkY = False

        # Jumping
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topRightY, topLeftY), obj.x, newY, False, isTwoAxis)

            if not chkY and checkY:
                checkY = False

        # Right
        if (speedX > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topRightX, bottomRightX), newX, newY, True, isTwoAxis)
            if not chkX and checkX:
                checkX = False

        # Left
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, (topLeftX, bottomLeftX), newX, newY, True, isTwoAxis)
            if not chkX and checkX:
                checkX = False

        return (checkX, checkY)

        # Check collision with other obj
        # SOON

    def checkTileCollision(self, mapManager, obj, corners, newX, newY, isXAxis, isTwoAxis):
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