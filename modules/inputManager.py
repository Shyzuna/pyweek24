"""
Title: inputManager File
Desc: Manage all the inputs
Creation Date: 15/10/17
LastMod Date: 16/10/17
TODO:
* sys.exit() ? or return value to go out of loop ?
"""

from objects.enums import ObjectName

import pygame
import sys

class InputManager(object):
    """
    This manager is all about the input stuff :
        * Updating events data
        * Apllying events on objects
    /!\ Should be instantiate once only
    """
    def __init__(self):
        """
        Not much to do here currently
        :return: Nothing
        """
        self.directionState = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
        }

    def handleFullScreen(self,displayManager,guiManager,event):
        """
        Check if input for fullscreen mode
        :param displayManager:
        :param guiManager:
        :param event:
        :return: Nothing
        """
        if event.key == pygame.K_F5:
            displayManager.toggleFullScreen(guiManager)

    def handleEvents(self,guiManager,displayManager):
        """
        Update events data and handle closing event
        :return: Nothing
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYUP:
                self.handleFullScreen(displayManager, guiManager,event)
                if event.key in self.directionState.keys():
                    self.directionState[event.key] = False
                elif event.key == pygame.K_RETURN:
                    guiManager.textBuffer.scrollNextText()
            elif event.type == pygame.KEYDOWN:
                if event.key in self.directionState.keys():
                    self.directionState[event.key] = True

    def handleMenuEvents(self,guiManager,displayManager):
        """
        Handle events for menu
        :return: Nothing
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYUP:

                self.handleFullScreen(displayManager, guiManager, event)

                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                elif event.key == pygame.K_UP:
                    guiManager.upButtonSelection()
                elif event.key == pygame.K_DOWN:
                    guiManager.downButtonSelection()
                elif event.key == pygame.K_SPACE:
                    # TODO use enum for button ?
                    if guiManager.currentButton == 0:
                        guiManager.startGame = True
                    elif guiManager.currentButton == 2:
                        sys.exit()

    def applyPlayerMoveEvents(self, managerList, deltaTime):
        """
        Apply moves inputs for current frame about the player
        :param managerList:
        :param deltaTime:
        :return: Nothing
        """
        mapManager = managerList["mapManager"]
        physicsManager = managerList["physicsManager"]
        scrollManager = managerList["scrollManager"]
        player = mapManager.objects[ObjectName.PLAYER]
        # Speed for the frame
        currentSpeed = (player.speed * deltaTime) / 1000
        distX,distY = 0,0
        if self.directionState[pygame.K_RIGHT]:
            distX += currentSpeed
        if self.directionState[pygame.K_LEFT]:
            distX -= currentSpeed

        # Check collision
        if physicsManager.checkCollision(mapManager,player,distX,distY):
            # Check is scrolling is needed
            scrollValue = scrollManager.isScrollNeeded(mapManager, player, distX, distY)
            if scrollValue:
                # Scroll Map
                mapManager.scrollMap(scrollValue)
            else:
                # Move player
                player.moveBy(distX,distY)

inputManager = InputManager()