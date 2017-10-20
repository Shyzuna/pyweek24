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
                scrollValue = scrollManager.isScrollNeeded(mapManager, object, speedX, speedY)
                if scrollValue:
                    # Scroll Map

                    if checkX and speedX != 0:
                        mapManager.scrollMap(scrollValue[0], 0)
                        if checkY:
                            object.y += speedY
                        else:
                            object.isOnGround = True

                    if checkY and speedY != 0:
                        mapManager.scrollMap(0, scrollValue[1])
                        if checkX:
                            object.x += speedX

                else:
                    if checkX:
                        object.x += speedX
                    if checkY:
                        object.y += speedY
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
        newX = obj.x + speedX + mapManager.currentRect.x
        newY = obj.y + speedY + mapManager.currentRect.y

        marge = 10

        topLeft = (newX + marge , newY + marge)
        topRight = (newX + obj.width - marge, newY + marge)
        bottomLeft = (newX + marge, newY + obj.height - marge)
        bottomRight = (newX + obj.width - marge, newY + obj.height - marge)

        top = [
            topLeft,
            topRight
        ]

        right = [
            topRight,
            bottomRight
        ]

        bottom = [
            bottomLeft,
            bottomRight
        ]

        left = [
            topLeft,
            bottomLeft
        ]

        checkX = True
        checkY = True

        # Falling
        if (speedY > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, bottom, newX, newY, False)
            if not chkX and checkX:
                checkX = False

            if not chkY and checkY:
                checkY = False

        # Jumping
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, top, newX, newY, False)
            if not chkX and checkX:
                checkX = False

            if not chkY and checkY:
                checkY = False

        # Right
        if (speedX > 0):
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, right, newX, newY, True)
            if not chkX and checkX:
                checkX = False

            if not chkY and checkY:
                checkY = False
        # Left
        else:
            (chkX, chkY) = self.checkTileCollision(mapManager, obj, left, newX, newY, True)
            if not chkX and checkX:
                checkX = False

            if not chkY and checkY:
                checkY = False

        return (checkX, checkY)

        # Check collision with other obj
        # SOON

    def checkTileCollision(self, mapManager, obj, corners, newX, newY, isXAxis):
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
                mapManager.tiles[tileY][tileX] = 'e'
                collision += 1

        if collision == 1:
           if not isXAxis:
               return (True, False)
        elif collision > 1:
            if isXAxis:
                return (False, True)
            else:
                return (True, False)

        return (True, True)

physicsManager = PhysicsManager()