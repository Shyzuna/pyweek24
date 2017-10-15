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

        self.displayedTiles = []
        self.startTile = 4
        self.isAnEnd = False

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
                x, y = int(x), int(y)
                #w, h = img[name].get_width(), img[name].get_height()
                w, h = 0, 1

                print(str(name) + " " + str(type) + " " + str(x) + " " + str(y) + " " + str(w))

                obj = None

                if type == objectType.GAME_OBJECT.value:
                    obj = gameObjects.GameObject(name, type, x, y, w, h)

                elif type == objectType.NINJA.value:
                    obj = gameObjects.Ninja(name, type, x, y, w, h)

                elif type == objectType.PLAYER.value:
                    obj = gameObjects.Player(name, type, x, y, w, h)

                elif type == objectType.TRAP.value:
                    obj = gameObjects.Trap(name, type, x, y, w, h)

                if obj is not None:
                    self.objects[name] = obj

                line = mapFile.readline()

            print(objectType.GAME_OBJECT.value)

        # Displayed tiles computation
        self.computeDisplayedTiles()

    def goToRight(self):
        """
        Moves starting index of displayed tiles to the right
        """
        if self.startTile < self.width - 1:
            self.startTile += 1
            self.computeDisplayedTiles()

    def goToLeft(self):
        """
        Moves starting index of displayed tiles to the left
        """
        if self.startTile > 0:
            self.startTile -= 1
            self.computeDisplayedTiles()

    def computeDisplayedTiles(self):
        """
        Computes tiles to display

        """

        self.displayedTiles = []

        # Left limit
        if self.startTile < settings.TILES_TO_DISPLAY and not self.isAnEnd:
            print('Left')
            for tilesLine in self.tiles:
                self.displayedTiles.append(tilesLine[:settings.TILES_TO_DISPLAY])

            self.isAnEnd = True

        # Right limit
        elif self.startTile  > (self.width - settings.TILES_TO_DISPLAY):
            print('Right')
            for tilesLine in self.tiles:
                self.displayedTiles.append(tilesLine[-settings.TILES_TO_DISPLAY:])

            self.isAnEnd = True

        # Middle of the map
        else:
            print('Middle')
            for tilesLine in self.tiles:
                self.displayedTiles.append(tilesLine[self.startTile:self.startTile + settings.TILES_TO_DISPLAY])

            self.isAnEnd = False

        print(self.startTile)
        print(self.displayedTiles)

mapManager = MapManager()






