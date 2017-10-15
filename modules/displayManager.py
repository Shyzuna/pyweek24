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
        pygame.display.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH,settings.SCREEN_HEIGHT))
        pygame.display.set_caption(settings.GAME_TITLE)

    def quit(self):
        pygame.display.quit()

    def display(self):
        """
        Display all elements
        :return: Nothing
        """

        # Clear screen
        self.screen.fill(Colors.BLACK)

        # Display stuff

        # Update screen
        pygame.display.flip()

displayManager = DisplayManager()