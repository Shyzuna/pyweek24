import os

from objects.enums import ObjectType as objectType
import objects.gameObjects as gameObjects
import settings.settings as settings

class MapManager:
    def __init__(self):
        """
        Constructor
        """

        self.width = 0
        self.height = 0
        self.tileWidth = 0
        self.tileHeight = 0
        self.objects = {}
        self.tiles = []
        self.dialogs = []

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

                x, y = pos.split('x')
                #w, h = img[name].get_width(), img[name].get_height()
                w, h = 0, 1

                print(str(name) + " " + str(type) + " " + str(x) + " " + str(y) + " " + str(w))

                obj = None

                if type == objectType.GAME_OBJECT:
                    obj = gameObjects.GameObject(name, type, x, y, w, h)

                elif type == objectType.NINJA:
                    obj = gameObjects.Ninja(name, type, x, y, w, h)

                elif type == objectType.PLAYER:
                    obj = gameObjects.player(name, type, x, y, w, h)

                elif type == objectType.TRAP:
                    obj = gameObjects.trap(name, type, x, y, w, h)

                if obj is not None:
                    self.objects[name] = obj

                line = mapFile.readline()

mapManager = MapManager()






