"""
Title: inputManager File
Desc: Manage all the inputs
Creation Date: 15/10/17
LastMod Date: 16/10/17
TODO:
* sys.exit() ? or return value to go out of loop ?
"""

from objects.enums import ObjectName,AnimationType
import settings.settings as settings

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

        self.jump_max = 500
        self.jumping = False

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

    def handleEvents(self, guiManager, displayManager):
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

    def handleMenuEvents(self, guiManager, displayManager):
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

        if player.isOnGround:
            if self.directionState[pygame.K_RIGHT]:
                player.velocityX = settings.MAX_VELOCITY_X
                player.animatedSprite.changeCurrentAnimation(AnimationType.WALKING)
            elif self.directionState[pygame.K_LEFT]:
                player.velocityX = -settings.MAX_VELOCITY_X
                player.animatedSprite.changeCurrentAnimation(AnimationType.WALKING)
            else:
                player.velocityX = 0
                player.animatedSprite.changeCurrentAnimation(AnimationType.IDLE)
        else:
            # Should be if only block ?
            if self.directionState[pygame.K_RIGHT]:
                player.velocityX = settings.MAX_VELOCITY_X / 2
            elif self.directionState[pygame.K_LEFT]:
                player.velocityX = -settings.MAX_VELOCITY_X / 2
            else:
                player.velocityX = 0
                player.animatedSprite.changeCurrentAnimation(AnimationType.IDLE)


        if self.directionState[pygame.K_UP]:
            if player.isOnGround:
                player.velocityY = -settings.MAX_VELOCITY_Y
                player.isOnGround = False

inputManager = InputManager()