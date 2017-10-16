"""
Title: physicsManager File
Desc: Used to manage phisics / collision
Creation Date: 16/10/17
LastMod Date: 16/10/17
TODO:
*
"""

import math

class PhysicsManager(object):
    def __init__(self):
        self.gravity = 100
        self.nonBlockingTiles = ['0']

    def applyGravity(self, mapManager, deltaTime):
        gravitySpeed = (self.gravity * deltaTime) / 1000
        for object in mapManager.objects.values():
            if self.checkCollision(mapManager,object,0,gravitySpeed):
                object.moveBy(0,gravitySpeed)

    def checkCollision(self, mapManager, obj, distX, distY):
        newX = obj.x + distX
        newY = obj.y + distY
        # Check collision with tiles
        return self.checkTileCollision(mapManager,obj,newX,newY)

        # Check collision with other obj
        # SOON

    def checkTileCollision(self, mapManager, obj, newX, newY):
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