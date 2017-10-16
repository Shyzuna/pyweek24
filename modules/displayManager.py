"""
Title: displayManager File
Desc: Init the display / display ALL the stuff
Creation Date: 15/10/17
LastMod Date: 15/10/17
TODO:
* LOOK FOR INIT FLAG (RESIZEABLE,FULLSCREEN...)
"""

import settings.settings as settings
from objects.enums import Colors

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

    def loadTiles(self,tileW,tileH):
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

    def display(self,mapManager):
        """
        Display all elements
        :return: Nothing
        """

        # Clear screen
        self.screen.fill(Colors.BLACK.value)

        # Display map
        ## TODO: Should use offset
        tileW,tileH = mapManager.tileWidth,mapManager.tileHeight
        startX = 0
        startY = 0
        for line in mapManager.displayedTiles:
            for tile in line:
                if tile != '0':
                    self.screen.blit(self.tilesImg[tile],(startX,startY))
                startX += tileW
            startY += tileH
            startX = 0


        # Update screen
        pygame.display.flip()

displayManager = DisplayManager()