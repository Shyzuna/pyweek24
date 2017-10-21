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
import random
import math

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
            img = pygame.image.load(os.path.join(settings.BG_PATH, str(i) + ".png"))
            currentW,currentH = img.get_size()
            # Reduce size of all images
            # TODO RATIO IN SETTINGS
            self.menuBg.append(pygame.transform.scale(img,(64,64)))

        # Create the background surface
        self.bg = pygame.Surface(self.screen.get_size())
        startX,startY = -10,-10
        screenW,screenH = self.screen.get_size()
        bgW,bgH = self.menuBg[0].get_size()
        j = 0
        while(startY < screenH):
             i = 0 if (j % 2) == 0 else 3
             while (startX < screenW):
                 self.bg.blit(self.menuBg[i],(startX,startY))
                 i = (i+2) % 4
                 startX += bgW
             startY += bgH
             startX = -10
             j += 1

        # TODO larger image and apply ration
        self.title = pygame.image.load(os.path.join(settings.MENU_PATH, "title.png"))

        # Loading buttons
        # TODO larger image and apply ration
        self.buttons = [
            pygame.image.load(os.path.join(settings.MENU_PATH, "jouer.png")),
            pygame.image.load(os.path.join(settings.MENU_PATH, "options.png")),
            pygame.image.load(os.path.join(settings.MENU_PATH, "quitter.png"))
        ]

        # Compute height interval
        i = 1
        totalH = self.title.get_size()[1]
        for button in self.buttons:
            buttonW,buttonH = button.get_size()
            totalH += buttonH
            i += 1
        self.interH = (self.screen.get_size()[1] - totalH) / (i+1)

        # Default values
        self.currentButton = 0
        self.totalButton = 3

    def upButtonSelection(self):
        """
        Modify current selected button in menu
        :return: Nothing
        """
        self.currentButton -= 1
        if self.currentButton < 0:
            self.currentButton = self.totalButton - 1

    def downButtonSelection(self):
        """
        Modify current selected button in menu
        :return: Nothing
        """
        self.currentButton = (self.currentButton + 1) % (self.totalButton)

    def updateScreen(self):
        """
        Update guiManager after a main change in config (like fullscreen)
        :return:
        """
        self.screen = pygame.display.get_surface()
        self.initMenu()

    def initHud(self):
        """
        Load elem for hud and create bar
        :return: Nothing
        """

        self.hudElem = {
            "hudBar": pygame.image.load(os.path.join(settings.HUD_PATH, "hudBar.png")),
            "ninjaIcon": pygame.image.load(os.path.join(settings.HUD_PATH, "ninjaIcon.png")),
            "ninjaIco": pygame.image.load(os.path.join(settings.HUD_PATH, "ninjaIco.png")),
            "deadIco": pygame.image.load(os.path.join(settings.HUD_PATH, "deadIco.png")),
        }

        # Resize Bar
        tmpHudElem = self.hudElem.copy()
        ratioX = settings.SCREEN_WIDTH / 1920
        ratioY = settings.SCREEN_HEIGHT / 1080
        # TODO: Have image for same resolution => cannot reduce all atm
        #for k,e in tmpHudElem.items():
        #    w,h = self.hudElem[k].get_size()
        #    self.hudElem[k] = pygame.transform.scale(e,(int(w * ratioX),int(h * ratioY)))

        w, h = self.hudElem["hudBar"].get_size()
        self.hudElem["hudBar"] = pygame.transform.scale(self.hudElem["hudBar"], (int(w * ratioX), int(h * ratioY) - 40))
        w, h = self.hudElem["hudBar"].get_size()

        # Init text buffer
        self.textBuffer = TextBuffer(w,h)

        # init Bars

        self.barHeight = 10
        self.barNumber = 3
        leftHeight = h - self.barNumber * self.barHeight
        self.innerSpace = leftHeight / (self.barNumber + 1)

        self.cooldownBars = []
        self.empoweringWaiting = -1
        self.loadSpeed = 10
        self.unloadSpeed = -25

        # draw default bar
        self.classicBar = pygame.Surface((w/5, self.barHeight))
        self.classicBar.fill(Colors.WHITE.value)
        self.classicBar.set_colorkey(Colors.WHITE.value)
        pygame.draw.rect(self.classicBar, Colors.BLACK.value, self.classicBar.get_rect(),2)

    def addNinjaBar(self):
        bar = {
            "displayed": True,
            "percent": 0,
            "alive": True,
            "empowering": False
        }
        self.cooldownBars.append(bar)

    def empowerSpell(self):
        """
        Try to empower next spell
        :return: True if ok else False
        """
        # Check if a bar is available
        i = 0
        for bar in self.cooldownBars:
            if bar["displayed"] and bar["alive"] and bar["percent"] == 100:
                self.empoweringWaiting = i
                return True
            i += 1
        return False

    def consumeWaitingEmpowering(self):
        """
        Activate the empowering status of the waiting
        :return:
        """
        self.cooldownBars[self.empoweringWaiting]["empowering"] = True
        self.empoweringWaiting = -1

    def updateBars(self, deltaTime):
        """
        Update the cooldowns bars
        :param deltaTime:
        :return:
        """
        currentLoadSpeed = (self.loadSpeed * deltaTime) / 1000
        currentUnloadSpeed = (self.unloadSpeed * deltaTime) / 1000
        for bar in self.cooldownBars:
            speed = currentLoadSpeed if not bar["empowering"] else currentUnloadSpeed
            bar["percent"] += speed
            if bar["percent"] > 100:
                bar["percent"] = 100
            elif bar["percent"] < 0:
                bar["empowering"] = False

    def drawInternBar(self, percent, isEmpowered):
        """
        draw the intern bar surface
        :param percent:
        :return: return bar surface
        """
        color = Colors.RED.value if isEmpowered else Colors.BLUE.value
        internBar = self.classicBar.copy()
        rect = internBar.get_rect()
        rect.width = (rect.width * percent ) / 100
        pygame.draw.rect(internBar, color, rect)
        return internBar

    def displayHud(self):
        """
        Display the in game hud
        :return: Nothing
        """
        screenW,screenH = self.screen.get_size()
        self.screen.blit(self.hudElem["hudBar"],(0,screenH - self.hudElem["hudBar"].get_size()[1]))

        startY = screenH - self.hudElem["hudBar"].get_size()[1] + 50
        startX = 20
        i = 0
        for bar in self.cooldownBars:
            if bar["displayed"]:
                ico = self.hudElem["ninjaIco"] if bar["alive"] else self.hudElem["deadIco"]
                self.screen.blit(ico,(startX,startY - ico.get_size()[1] / 2))
                startX += ico.get_size()[0] + 20
                empowering = bar["empowering"] or i == self.empoweringWaiting
                self.screen.blit(self.drawInternBar(bar["percent"], empowering), (startX, startY))
                self.screen.blit(self.classicBar, (startX,startY))
                startY += self.barHeight + self.innerSpace
                startX = 20
            i += 1
        self.textBuffer.display(self.screen)

    def displayMenu(self):
        """
        Display menu elements
        :return: Nothing
        """

        # Clear screen
        self.screen.fill(Colors.BLACK.value)

        screenW, screenH = self.screen.get_size()

        # Display BG
        self.screen.blit(self.bg, (0, 0))

        # Display title
        titleW,titleH = self.title.get_size()
        posX = (screenW - titleW) / 2
        posY = self.interH
        self.screen.blit(self.title,(posX,posY))
        posY += titleH + self.interH

        # TODO smth better for the mark ?
        # Display button + selected mark
        i = 0
        highlightSize = 4
        for button in self.buttons:
            buttonW, buttonH = button.get_size()
            posX = (screenW - buttonW) / 2
            if self.currentButton == i:
                rect = button.get_rect()
                rect.width += highlightSize * 2
                rect.height += highlightSize * 2
                selected = pygame.Surface((rect.width,rect.height))
                pygame.draw.rect(selected,Colors.YELLOW.value,rect)
                self.screen.blit(selected, (posX - highlightSize, posY - highlightSize))
            self.screen.blit(button, (posX, posY))
            posY += button.get_size()[1] + self.interH
            i += 1

        # Update screen
        pygame.display.flip()

    def updateHud(self,deltaTime):
        """
        Update the hud
        :param deltaTime:
        :return: Nothing
        """
        self.textBuffer.applyScrolling(deltaTime)
        self.updateBars(deltaTime)

class TextBuffer(object):
    """
    Manage the text zone to render dialog and all
    """
    def __init__(self, hudW, hudH):
        """
        Init the text buffer
        """

        pygame.font.init()

        self.fontSize = 20

        self.font = pygame.font.Font(os.path.join(settings.FONTS_PATH,"arial.ttf"), self.fontSize)

        # define circular list
        self.textsList = []
        self.maxTexts = 25
        self.topIndex = 0
        self.nextIndex = 0
        for i in range (0,25):
            self.textsList.append(None)

        # Not just magic value => percentage
        self.offsetX = int(hudW * 0.025)
        self.offsetY = int(hudH * 0.06)

        self.textZoneW = int(hudW * 0.625) - self.offsetX
        self.textZoneH = int(hudH * 0.56) - self.offsetY

        self.textZoneX = settings.SCREEN_WIDTH - self.textZoneW - (self.offsetX)
        self.textZoneY = (settings.SCREEN_HEIGHT - self.textZoneH) - (self.offsetY / 2)

        # Create text zone
        self.textZoneSurface = pygame.Surface((self.textZoneW,self.textZoneH))
        self.textZoneSurface.fill(Colors.WHITE.value)
        self.textZoneSurface.set_colorkey(Colors.WHITE.value)
        self.displayZoneRect = False

        # Approximate max size
        nonce = "test sentence"
        w, h = self.font.size(nonce)
        self.maxCharacter = math.floor((self.textZoneW * len(nonce)) / w)
        self.maxLine = math.floor(self.textZoneH / h)
        self.textHeight = h

        # Scrolling info
        self.scrollSpeed = 50
        self.isScrolling = False
        self.scrollingOffsetY = 0
        self.scrollingNumber = 0

        # Carret surface for scrolling
        # TODO: Maybe improve to non static values
        self.displayCarret = False
        self.carretSurface = pygame.Surface((15,15))
        self.carretSurface.fill(Colors.WHITE.value)
        self.carretSurface.set_colorkey(Colors.WHITE.value)
        pointList = [
            (0,0),
            (15,0),
            (7.5,15)
        ]
        pygame.draw.polygon(self.carretSurface,Colors.BLACK.value,pointList)
        self.carretX = settings.SCREEN_WIDTH - 15
        self.carretY = settings.SCREEN_HEIGHT - 15


    def renderText(self, text):
        """
        Create a text surface and add it to the queue
        /!\ doest work with text monoblock with size gt self.maxCharacter
        :param text:
        :return: Nothing
        """
        if len(text) > self.maxCharacter:
            splitText = text.split(" ")
            currentString = ""
            for word in splitText:
                if len(currentString) + len(word) + 1 < self.maxCharacter:
                    currentString += " " + word
                else:
                    textSurface = self.font.render(currentString[1:], 1, Colors.BLACK.value)
                    self.appendTextToList(textSurface)
                    currentString = " " + word
            textSurface = self.font.render(currentString[1:], 1, Colors.BLACK.value)
            self.appendTextToList(textSurface)
        else:
            textSurface = self.font.render(text, 1, Colors.BLACK.value)
            self.appendTextToList(textSurface)

    def appendTextToList(self, textSurface):
        """
        Append a text surface to circular list
        :param textSurface:
        :return: nothing
        """
        self.textsList[self.nextIndex] = textSurface
        self.nextIndex = (self.nextIndex + 1) % self.maxTexts

    def scrollNextText(self, scrollTime=1):
        """
        increase scroll number is possible
        :return: Nothing
        """
        size = abs(self.nextIndex - self.topIndex)
        if (self.scrollingNumber + scrollTime) <= size:
            self.scrollingNumber += scrollTime
            self.isScrolling = True

    def applyScrolling(self,deltaTime):
        """
        Apply the scrolling if activated using delta time
        :param deltaTime:
        :return: Nothing
        """
        if self.isScrolling:
            self.scrollingOffsetY += (self.scrollSpeed * deltaTime) / 1000
            if self.scrollingOffsetY > self.textHeight:
                self.topIndex = (self.topIndex + 1) % self.maxTexts
                self.scrollingOffsetY = 0
                self.scrollingNumber -= 1
                if self.scrollingNumber == 0:
                    self.isScrolling = False

    def display(self, screen):
        """
        Display the text zone with limited text number
        :param screen:
        :return: Nothing
        """
        self.textZoneSurface.fill(Colors.WHITE.value)
        j = 0
        startY = - self.scrollingOffsetY
        for i in range(self.topIndex,self.nextIndex):
            j += 1
            if j > (self.maxLine + 1):
                break
            self.textZoneSurface.blit(self.textsList[i],(0,startY))
            startY += self.textHeight

        if self.displayZoneRect:
            rect = pygame.Rect(0, 0, self.textZoneW, self.textZoneH)
            pygame.draw.rect(self.textZoneSurface, Colors.BLACK.value, rect, 3)
        screen.blit(self.textZoneSurface,(self.textZoneX,self.textZoneY))

        if abs(self.nextIndex - self.topIndex) > 0:
            screen.blit(self.carretSurface,(self.carretX,self.carretY))

guiManager = GUIManager()