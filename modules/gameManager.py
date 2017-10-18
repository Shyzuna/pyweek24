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
from modules.PhysicsManager import physicsManager
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
        Init clock / FPS / manager list
        :return: Nothing
        """
        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = settings.FPS
        self.showFps = True

        self.managerList = {
            "displayManager": displayManager,
            "inputManager": inputManager,
            "guiManager": guiManager,
            "mapManager": mapManager,
            "scrollManager": scrollManager,
            "physicsManager": physicsManager,
        }


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
        displayManager.createMapSurface(mapManager)

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
        """
        Loop for the menu
        :return: Noothing
        """
        inputManager.handleMenuEvents(guiManager,displayManager)
        if guiManager.startGame:
            self.done = True
        guiManager.displayMenu()

    def gameLoop(self):
        """
        Loop for the game
        :return: Nothing
        """
        inputManager.handleEvents(guiManager, displayManager)
        inputManager.applyPlayerMoveEvents(self.managerList, self.deltaTime)
        physicsManager.computeVelocity(mapManager, scrollManager, self.deltaTime)
        physicsManager.applyGravity(mapManager)
        displayManager.display(mapManager,guiManager)

gameManager = GameManager()