"""
Title: displayManager File
Desc: Init the display / display ALL the stuff
Creation Date: 15/10/17
LastMod Date: 16/10/17
TODO:
* LOOK FOR INIT FLAG (RESIZEABLE,FULLSCREEN...)
"""

import settings.settings as settings
from objects.enums import Colors,ObjectName
from settings.objectSettings import objectProperties

import pygame
import string
import os

class DisplayManager(object):
    """
    This manager is all about the display stuff :
        * Init
        * Displaying
    /!\ Should be instantiate once only
    """

    def __init__(self):
        """
        Not much to do currently
        :return: Nothing
        """
        pass

    def init(self):
        """
        Init the lib/screen with settings file
        :return:
        """
        self.flags = pygame.DOUBLEBUF
        pygame.display.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT),
                                              self.flags)
        pygame.display.set_caption(settings.GAME_TITLE)
        self.isFullscreen = False

    def loadTilesImg(self,tileW,tileH):
        """
        Load all the tiles
        :return: Nothing
        """
        self.tilesImg = {}
        for l in string.ascii_lowercase:
            try:
                img = pygame.image.load(os.path.join(settings.TILES_PATH,l + ".png"))
                self.tilesImg[l] = pygame.transform.scale(img,(tileW,tileH))
            except:
                pass
        for i in range(1,10):
            try:
                img = pygame.image.load(os.path.join(settings.TILES_PATH,str(i) + ".png"))
                self.tilesImg[str(i)] =  pygame.transform.scale(img,(tileW,tileH))
            except:
                pass


        self.menuBg = []
        for i in range(0,4):
            img = pygame.image.load(os.path.join(settings.BG_PATH, str(i) + ".png"))
            currentW,currentH = img.get_size()
            # Reduce size of all images
            # TODO RATIO IN SETTINGS
            self.menuBg.append(pygame.transform.scale(img,(64,64)))

    def createMapSurface(self, mapManager):
        """
        Create the full map surface (See if it's worth ?)
        :param mapManager:
        :return: Nothing
        """

        self.mapSurface = pygame.Surface((mapManager.mapSizeX, mapManager.mapSizeY))
        self.mapSurface.fill(Colors.WHITE.value)

        # SET BG
        startX,startY = -10,-10
        screenW,screenH = self.screen.get_size()
        bgW,bgH = self.menuBg[0].get_size()
        j = 0
        while(startY <  mapManager.mapSizeY):
             i = 0 if (j % 2) == 0 else 3
             while (startX < mapManager.mapSizeX):
                 self.mapSurface.blit(self.menuBg[i],(startX,startY))
                 i = (i+2) % 4
                 startX += bgW
             startY += bgH
             startX = -10
             j += 1

        # Set Map
        tileW,tileH = mapManager.tileWidth,mapManager.tileHeight
        startX = 0
        startY = 0
        for line in mapManager.tiles:
            for tile in line:
                if tile != '0':
                    self.mapSurface.blit(self.tilesImg[tile],(startX,startY))
                startX += tileW
            startY += tileH
            startX = 0

    def loadObjectsImg(self,mapManager):
        """
        Load all images for objects and set width and height of them (maybe smwhere else ?)
        :param mapManager:
        :return: Nothing
        """
        self.objectsImg = {}
        for object in mapManager.objects.values():
            print(object.name)
            if object.name not in self.objectsImg.keys():
                img = pygame.image.load(objectProperties[object.name]['imgPath'])
                w,h = img.get_size()
                ratio = objectProperties[object.name]['imgRatio']
                self.objectsImg[object.name] = pygame.transform.scale(img,(int(w/ratio),int(h/ratio)))
            w,h = self.objectsImg[object.name].get_size()
            object.width = w
            object.height = h
            if object.name in [ObjectName.PLAYER,ObjectName.NINJA]:
                object.initSpriteSheet()

    def toggleFullScreen(self,guiManager):
        """
        Change fullscreen mode
        :return: Nothing
        """
        self.isFullscreen = not self.isFullscreen
        flags = pygame.FULLSCREEN|pygame.HWSURFACE if self.isFullscreen else self.flags
        if flags:
            self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT),
                                              flags)
        else:
            self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        guiManager.updateScreen()

    def quit(self):
        """
        Used to exit the game and close display
        :return: Nothing
        """
        pygame.display.quit()

    def display(self,mapManager,guiManager):
        """
        Display all elements
        :return: Nothing
        """
        # Clear screen
        self.screen.fill(Colors.WHITE.value)

        # Display part of map
        self.screen.blit(self.mapSurface, (0, 0), mapManager.currentRect)

        for object in mapManager.objects.values():
            object.blit(self.screen,self.objectsImg)

        guiManager.displayHud()

        # Update screen
        pygame.display.flip()

displayManager = DisplayManager()