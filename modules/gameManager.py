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
from modules.physicsManager import physicsManager
from modules.scrollManager import scrollManager
from modules.soundManager import soundManager
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
        pass

    def init(self, isIntroFinished):
        """
        Init stuff
        :return: Nothing
        """

        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = settings.FPS
        self.showFps = True
        self.introFinished = isIntroFinished
        self.gameWin = False

        self.managerList = {
            "displayManager": displayManager,
            "inputManager": inputManager,
            "guiManager": guiManager,
            "mapManager": mapManager,
            "scrollManager": scrollManager,
            "physicsManager": physicsManager,
            "soundManager": soundManager
        }

        inputManager.init()
        mapManager.init()
        displayManager.init()
        soundManager.init()
        guiManager.init()
        guiManager.initHud()
        mapManager.load('test.map',[])
        displayManager.loadTilesImg(mapManager.tileWidth,mapManager.tileHeight)
        displayManager.createMapSurface(mapManager)
        self.player = mapManager.objects["player1"]

    def start(self):
        """
        Start the menu, then the game or quit
        :return: Nothing
        """
        # TODO smth better ?
        while 1:
            self.mainLoop(self.menuLoop)
            self.mainLoop(self.gameLoop)
            self.init(True)

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
        inputManager.handleMenuEvents(guiManager, displayManager)
        if guiManager.startGame:
            self.done = True
        guiManager.displayMenu()

    def gameLoop(self):
        """
        Loop for the game
        :return: Nothing
        """

        if guiManager.endofGame or self.gameWin:
            self.player.disabled = True
            self.player.animatedSprite.changeCurrentAnimation(AnimationType.DEAD)

        inputManager.handleEvents(guiManager, displayManager, mapManager, self)
        self.done = inputManager.exitLoop

        if self.introFinished:
            inputManager.applyPlayerMoveEvents(self.managerList, self.deltaTime)

        if not guiManager.endofGame and not self.gameWin:
            physicsManager.applyGravity(mapManager)
            physicsManager.applyFriction(mapManager)
            physicsManager.computeVelocity(mapManager, scrollManager, guiManager, self.deltaTime)
            dialogList = physicsManager.checkDialogCollision(mapManager)
            for dialog in dialogList:
                if not (self.introFinished and dialog.name == settings.INTRO_DIALOG_ID):
                    dialog.play(guiManager)

            mapManager.updateDialogs(guiManager, self.deltaTime, self)

        if not self.gameWin:
            for object in mapManager.objects.values():
                object.animatedSprite.playAnimation(self.deltaTime)

            guiManager.updateHud(self.deltaTime)
            displayManager.display(mapManager,guiManager)
        else:
            displayManager.displayEndScreen(mapManager)


gameManager = GameManager()