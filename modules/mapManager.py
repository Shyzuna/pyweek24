import os

from objects.enums import ObjectType as objectType
from objects.enums import ObjectName as objectName
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
        self.startTileX = settings.DELTA_TILES_TO_DISPLAY_X
        self.startTileY = settings.DELTA_TILES_TO_DISPLAY_Y
        self.totalTilesToDisplayX = 0
        self.totalTilesToDisplayY = 0
        self.isAnEndX = False
        self.isAnEndY = False

        self.currentOffsetX = 0
        self.currentOffsetY = 0

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

        # Compute tiles to display
        settings.TILES_TO_DISPLAY_X = int(settings.SCREEN_WIDTH / self.tileWidth)
        settings.TILES_TO_DISPLAY_Y = int(settings.SCREEN_HEIGHT / self.tileHeight)

        self.totalTilesToDisplayX = settings.TILES_TO_DISPLAY_X + settings.DELTA_TILES_TO_DISPLAY_X
        self.totalTilesToDisplayY = settings.TILES_TO_DISPLAY_Y + settings.DELTA_TILES_TO_DISPLAY_Y

        print("Tile to display X: " + str(settings.TILES_TO_DISPLAY_X))
        print("Tile to display Y: " + str(settings.TILES_TO_DISPLAY_Y))

        # Displayed tiles computation
        self.computeDisplayedTiles()

    def goToRight(self):
        """
        Moves starting index of displayed tiles to the right
        """

        if self.currentOffsetX > -self.tileWidth:
            self.currentOffsetX -= settings.SCROLL_SPEED
        elif self.startTileX < self.width - self.totalTilesToDisplayX:
                self.startTileX += 1
                self.computeDisplayedTiles()
                self.currentOffsetX = 0

    def goToLeft(self):
        """
        Moves starting index of displayed tiles to the left
        """

        if self.currentOffsetX < self.tileWidth:
            self.currentOffsetX += settings.SCROLL_SPEED
        elif self.startTileX > settings.DELTA_TILES_TO_DISPLAY_X:
            self.startTileX -= 1
            self.computeDisplayedTiles()
            self.currentOffsetX = 0

    def goUp(self):
        """
        Moves starting index of displayed tiles up
        """

        if self.currentOffsetY < self.tileHeight:
            self.currentOffsetY += settings.SCROLL_SPEED
        elif self.startTileY > settings.DELTA_TILES_TO_DISPLAY_Y:
            self.startTileY -= 1
            self.computeDisplayedTiles()
            self.currentOffsetY = 0

    def goDown(self):
        """
        Moves starting index of displayed tiles up
        """

        if self.currentOffsetY > -self.tileHeight:
            self.currentOffsetY -= settings.SCROLL_SPEED
        elif self.startTileY < self.height - self.totalTilesToDisplayY:
                self.startTileY += 1
                self.computeDisplayedTiles()
                self.currentOffsetX = 0

    def computeDisplayedTiles(self):
        """
        Computes tiles to display

        """

        self.displayedTiles = []
        cutLeft = self.startTileX - settings.DELTA_TILES_TO_DISPLAY_X
        cutRight = self.startTileX + self.totalTilesToDisplayX
        cutUp = self.startTileY - settings.DELTA_TILES_TO_DISPLAY_Y
        cutDown = self.startTileY+ self.totalTilesToDisplayY

        print("left : " + str(cutLeft))
        print("right : " + str(cutRight))
        print("up : " + str(cutUp))
        print("down : " + str(cutDown))
        self.displayedTiles = [row[cutLeft:cutRight] for row in self.tiles[cutUp:cutDown]]
        print(self.startTileX)
        print(self.displayedTiles)

mapManager = MapManager()






