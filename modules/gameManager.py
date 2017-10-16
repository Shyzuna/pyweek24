"""
Title: gameManager File
Desc: Used to start the game
Creation Date: 16/10/17
LastMod Date: 16/10/17
TODO:
* Maybe other transition for menu => loop (especially if we want to return at menu)
"""

from modules.displayManager import displayManager
from modules.inputManager import inputManager
from modules.guiManager import guiManager
from modules.mapManager import mapManager
from modules.scrollManager import scrollManager
import settings.settings as settings

from objects.enums import *

import pygame
import math

class GameManager(object):
    """
    This manager is all about the Game stuff :
        * Game loop
        * Menu loop
    /!\ Should be instantiate once only
    """
    def __init__(self):
        """
        Nothing much to do currently
        :return: Nothing
        """
        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = settings.FPS
        self.showFps = True

    def init(self):
        """
        Init stuff
        :return: Nothing
        """
        displayManager.init()
        guiManager.init()
        mapManager.load('test.map',[])
        displayManager.loadTilesImg(mapManager.tileWidth,mapManager.tileHeight)
        displayManager.loadObjectsImg(mapManager)

    import os

    # Path
    MAPS_PATH = os.path.join('data', 'maps')
    IMGS_PATH = os.path.join('data', 'imgs')
    TILES_PATH = os.path.join(IMGS_PATH, 'tiles')
    BG_PATH = os.path.join(IMGS_PATH, 'background')
    MENU_PATH = os.path.join(IMGS_PATH, 'menu')

    # Display
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 60

    # Number of tiles to display
    TILES_TO_DISPLAY_WIDTH = 2
    TILES_TO_DISPLAY_HEIGHT = 2

    # Delta number of tiles
    DELTA_TILES_TO_DISPLAY_WIDTH = 2
    DELTA_TILES_TO_DISPLAY_HEIGHT = 2

    # Scroll zone (in pixels)
    SCROLL_ZONE = 2

    # Important
    GAME_TITLE = "Beyond the game"

    # Other
    DATA_DELIMITER = '------'
    def start(self):
        """
        Start the menu, then the game or quit
        :return: Nothing
        """
        # TODO smth better ?
        self.mainLoop(self.menuLoop)
        self.mainLoop(self.gameLoop)

    def mainLoop(self,loop):
        """
        Just a loop wrapper for now
        :param loop: loop function
        :return: Nothing
        """
        self.done = False
        while not self.done:
            self.clock.tick(self.fps)
            self.deltaTime = self.clock.get_time()
            loop()
            if self.showFps:
                pygame.display.set_caption(str(round(self.clock.get_fps(),2)) + " - " + settings.GAME_TITLE)

    def menuLoop(self):
        inputManager.handleMenuEvents(guiManager,displayManager)
        if guiManager.startGame:
            self.done = True
        guiManager.displayMenu()

    def gameLoop(self):
        # TODO: Test si l'on est en mouvement pour éviter de lancer pour rien
        #scrollManager.checkPlayerPosition(mapManager)
        inputManager.handleEvents(guiManager,displayManager)
        displayManager.display(mapManager)

gameManager = GameManager()