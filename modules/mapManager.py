"""
Title: mapManager File
Desc: Manage the map loading and scrolling and other objects
Creation Date: 15/10/17
LastMod Date: 16/10/17
TODO:
*
"""

import os
import pygame

from objects.enums import ObjectType as objectType
from objects.enums import ObjectName as objectName
import objects.gameObjects as gameObjects
import settings.settings as settings

class MapManager:
    """
    This manager is all about the map stuff :
        * Loading
        * Moving map for scrolling
    /!\ Should be instantiate once only
    """

    def __init__(self):
        """
        Constructor
        """

        self.width = 0
        self.height = 0
        self.tileWidth = 0
        self.tileHeight = 0
        self.mapSizeX = 0
        self.mapSizeY = 0
        self.objects = {}
        self.tiles = []
        self.dialogs = []
        self.currentRect = pygame.Rect(0, 0, settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)

    def load(self, name, img):
        """
        Loads a map

        :param name: name of map
        :param img: list of sprites
        """

        with open(os.path.join(settings.MAPS_PATH, name)) as mapFile:
            # Size of map
            line = mapFile.readline()
            width, height = line.split('x')
            self.width = int(width)
            self.height = int(height)

            # Size of tiles
            line = mapFile.readline()
            tileWidth, tileHeight = line.split('x')
            self.tileWidth = int(tileWidth)
            self.tileHeight = int(tileHeight)

            # Total size of map in pixel
            self.mapSizeX = self.width * self.tileWidth
            self.mapSizeY = self.height * self.tileHeight

            # Tiles
            print("tiles")
            mapFile.readline()
            line = mapFile.readline()
            while settings.DATA_DELIMITER not in line:
                self.tiles.append(list(line.rstrip()))
                line = mapFile.readline()

            print(self.tiles)

            # Dialogs
            print("dialogs")
            line = mapFile.readline()
            while settings.DATA_DELIMITER not in line:
                self.dialogs.append(list(line.rstrip()))
                line = mapFile.readline()

            print(self.dialogs)

            # Objects
            line = mapFile.readline()
            while settings.DATA_DELIMITER not in line:
                line = line.rstrip()
                name, type, pos = line.split('|')
                name = objectName(name)
                type = objectType(type)

                tileX, tileY = pos.split('x')
                tileX, tileY = int(tileX), int(tileY)
                x,y = tileX * self.tileWidth, tileY * self.tileHeight
                #w, h = img[name].get_width(), img[name].get_height()
                w, h = 0, 1

                print(str(name) + " " + str(type) + " " + str(x) + " " + str(y) + " " + str(w))

                obj = None

                if type == objectType.GAME_OBJECT:
                    obj = gameObjects.GameObject(name, type, x, y, tileX, tileY, w, h)

                elif type == objectType.NINJA:
                    obj = gameObjects.Ninja(name, type, x, y, tileX, tileY, w, h)

                elif type == objectType.PLAYER:
                    obj = gameObjects.Player(name, type, x, y, tileX, tileY, w, h)

                elif type == objectType.TRAP:
                    obj = gameObjects.Trap(name, type, x, y, tileX, tileY, w, h)

                if obj is not None:
                    self.objects[name] = obj

                line = mapFile.readline()

            print(objectType.GAME_OBJECT.value)


    def scrollMap(self, x, y):
        """
        Try to scroll the map by scrollValue if possible
        :param scrollValue:
        :return: Nothing
        """
        self.currentRect.x += x
        self.currentRect.y += y

mapManager = MapManager()






