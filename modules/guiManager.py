"""
Title: guiManager File
Desc: Manage all the stuff GUI to display
Creation Date: 15/10/17
LastMod Date: 15/10/17
TODO:
*
"""

import settings.settings as settings
from objects.enums import Colors

import pygame

class GUIManager(object):
    """
    This manager is all about the GUI stuff :
        * Menu
        * HUD
    /!\ Should be instantiate once only
    /!\ After the displayManager
    """

    def __init__(self):
        """
        Check if display already init and get the screen
        :return: Nothing
        """
        if not pygame.display.get_init() or not pygame.display.get_surface():
            raise RuntimeError("Display not initialize")

        self.screen = pygame.display.get_surface()

        # If at the menu
        self.inStartMenu = True
        self.startGame = False

    def displayMenu(self):
        """
        Display menu elements
        :return: Nothing
        """

        # Clear screen
        self.screen.fill(Colors.BLACK)

        # Display stuff

        # Update screen
        pygame.display.flip()


guiManager = GUIManager()