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
        scrollManager.checkPlayerPosition(mapManager)
        inputManager.handleEvents(guiManager,displayManager)
        displayManager.display()

gameManager = GameManager()