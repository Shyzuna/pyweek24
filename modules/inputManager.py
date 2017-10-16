"""
Title: inputManager File
Desc: Manage all the inputs
Creation Date: 15/10/17
LastMod Date: 15/10/17
TODO:
* sys.exit() ? or return value to go out of loop ?
"""

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
        pass

    def handleEvents(self):
        """
        Update events data and handle closing event
        :return: Nothing
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

    def handleMenuEvents(self,guiManager):
        """
        Handle events for menu
        :return: Nothing
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYUP:
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

inputManager = InputManager()