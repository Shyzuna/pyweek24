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
            speedY = (object.velocityY * deltaTime) / 1000
            speedX = (object.velocityX * deltaTime) / 1000

            (checkX, checkY) = self.checkCollision(mapManager, object, speedX, speedY)

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

        topLeft = (newX, newY)
        topRight = (newX + obj.width, newY)
        bottomLeft = (newX, newY + obj.height)
        bottomRight = (newX + obj.width, newY + obj.height)

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

        cornerL = [
            (newX, newY),
            (newX + obj.width, newY),
            (newX, newY + obj.height),
            (newX + obj.width, newY + obj.height)
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

        for tuple in corners:
            tileX = math.floor(tuple[0] / mapManager.tileWidth)
            tileY = math.floor(tuple[1] / mapManager.tileHeight)

            if tileX >= mapManager.width or tileY >= mapManager.height:
                return (False, False)

            if mapManager.tiles[tileY][tileX] not in self.nonBlockingTiles:
                collision += 1

        if collision > 1:
            if isXAxis:
                return (False, True)
            else:
                return (True, False)
        else:
            return (True, True)

physicsManager = PhysicsManager()