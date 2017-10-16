"""
Title: guiManager File
Desc: Manage all the stuff GUI to display
Creation Date: 15/10/17
LastMod Date: 15/10/17
TODO:
* RATIO for image resizing in settings
"""

import settings.settings as settings
from objects.enums import Colors

import pygame
import os

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
        Nothing much to do here
        :return: Nothing
        """
        pass

    def init(self):
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

        self.initMenu()

    def initMenu(self):
        # Loading BG
        self.menuBg = []

        ratio = settings.SCREEN_WIDTH / settings.SCREEN_HEIGHT

        for i in range(0,4):
            img = pygame.image.load(os.path.join(settings.IMGS_PATH, "BGTile" + str(i) + ".png"))
            currentW,currentH = img.get_size()
            # Reduce size of all images
            # TODO RATIO IN SETTINGS
            self.menuBg.append(pygame.transform.scale(img,(64,64)))

        # TODO larger image and apply ration
        self.title = pygame.image.load(os.path.join(settings.IMGS_PATH, "title.png"))

        # Loading buttons
        # TODO larger image and apply ration
        self.buttons = [
            pygame.image.load(os.path.join(settings.IMGS_PATH, "jouer.png")),
            pygame.image.load(os.path.join(settings.IMGS_PATH, "options.png")),
            pygame.image.load(os.path.join(settings.IMGS_PATH, "quitter.png"))
        ]

        # Default values
        self.currentButton = 0
        self.totalButton = 3

    def upButtonSelection(self):
        self.currentButton -= 1
        if self.currentButton < 0:
            self.currentButton = self.totalButton - 1

    def downButtonSelection(self):
        self.currentButton = (self.currentButton + 1) % (self.totalButton)

    def displayMenu(self):
        """
        Display menu elements
        :return: Nothing
        """
        # TODO move position computing in init

        # Clear screen
        self.screen.fill(Colors.BLACK.value)

        # Display BG
        startX,startY = -10,-10
        screenW,screenH = self.screen.get_size()
        bgW,bgH = self.menuBg[0].get_size()
        j = 0
        while(startY < screenH):
            i = 0 if (j % 2) == 0 else 3
            while (startX < screenW):
                self.screen.blit(self.menuBg[i],(startX,startY))
                i = (i+2) % 4
                startX += bgW
            startY += bgH
            startX = -10
            j += 1

        # Display title
        titleW,titleH = self.title.get_size()
        posX = (screenW - titleW) / 2
        # Compute height interval
        i = 1
        totalH = titleH
        for button in self.buttons:
            buttonW,buttonH = button.get_size()
            totalH += buttonH
            i += 1
        interH = (screenH - totalH) / (i+1)
        posY = interH
        self.screen.blit(self.title,(posX,posY))
        posY += titleH + interH

        # TODO smth better for the mark ?
        # Display button + selected mark
        posX = (screenW - buttonW) / 2
        i = 0
        highlightSize = 4
        for button in self.buttons:
            if self.currentButton == i:
                rect = button.get_rect()
                rect.width += highlightSize * 2
                rect.height += highlightSize * 2
                selected = pygame.Surface((rect.width,rect.height))
                pygame.draw.rect(selected,Colors.YELLOW.value,rect)
                self.screen.blit(selected, (posX - highlightSize, posY - highlightSize))
            self.screen.blit(button, (posX, posY))
            posY += button.get_size()[1] + interH
            i += 1

        # Update screen
        pygame.display.flip()


guiManager = GUIManager()