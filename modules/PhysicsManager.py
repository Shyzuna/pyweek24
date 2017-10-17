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

    def applyGravity(self, mapManager, scrollManager, deltaTime):
        """
        Apply gravity on all objects with scrolling handling for player
        :param mapManager:
        :param scrollManager:
        :param deltaTime:
        :return: Nothing
        """
        gravitySpeed = (self.gravity * deltaTime) / 1000
        for object in mapManager.objects.values():
            if self.checkCollision(mapManager,object,0,gravitySpeed):
                if object.name == ObjectName.PLAYER:
                    scrollValue = scrollManager.isScrollNeeded(mapManager, object, 0, gravitySpeed)
                    if scrollValue:
                        # Scroll Map
                        mapManager.scrollMap(scrollValue)
                    else:
                        # Move player
                        object.moveBy(0, gravitySpeed)
                else:
                    object.moveBy(0,gravitySpeed)

    def checkCollision(self, mapManager, obj, distX, distY):
        """
        Check tile and object collision for an object
        :param mapManager:
        :param obj:
        :param distX:
        :param distY:
        :return: True/False if can move or not
        """
        # Get future position on global map
        newX = obj.x + distX + mapManager.currentRect.x
        newY = obj.y + distY + mapManager.currentRect.y
        # Check collision with tiles
        return self.checkTileCollision(mapManager,obj,newX,newY)

        # Check collision with other obj
        # SOON

    def checkTileCollision(self, mapManager, obj, newX, newY):
        """
        Check tile collision of the object
        :param mapManager:
        :param obj:
        :param newX:
        :param newY:
        :return: True/False if can move or not
        """
        cornerL = [
            (newX,newY),
            (newX + obj.width, newY),
            (newX, newY + obj.height),
            (newX + obj.width, newY + obj.height)
        ]
        for x,y in cornerL:
            tileX = math.floor(x / mapManager.tileWidth)
            tileY = math.floor(y / mapManager.tileHeight)
            if mapManager.tiles[tileY][tileX] not in self.nonBlockingTiles:
                return False
        return True

physicsManager = PhysicsManager()