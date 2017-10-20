"""
Title: Animation object
Desc: Animation object to handle sprite animation
Creation Date: 20/10/17
LastMod Date: 20/10/17
TODO:
*
"""

import pygame

class AnimatedSprite(object):
    """
    Animated sprite object for animate the objects
    This use spritesheet
    """
    def __init__(self, spriteSheet, maxSpriteW, maxSpriteH, scaleX=1, scaleY=1):
        """
        Init info for AnimatedSprite
        :param spriteSheet:
        :param imgW:
        :param imgH:
        :param scaleX:
        :param scaleY:
        """

        # Image info
        self.spriteSheet = spriteSheet
        w,h = spriteSheet.get_size()
        self.imgW = w // maxSpriteW
        self.imgH = h // maxSpriteH
        self.scaleX = scaleX
        self.scaleY = scaleY

        # Global animation data
        self.defaultAnim = None
        self.currentAnim = None
        self.animeList = {}

        # Playing information data
        self.currentSprite = 0
        self.currentTime = 0
        self.currentRect = None

    def addAnimation(self, name, spriteNumber, direction, line, isDefault, timeDuration=-1):
        """
        Load a new animation
        :param name:
        :param spriteNumber:
        :param direction:
        :param isDefault:
        :param timeDuration: in ms (-1 is for one image)
        :return: Nothing

        /!\ doesnt handle direction for now just left to right

        """
        self.animeList[name] = {
            "spriteNumber": spriteNumber,
            "line": line,
 #           "direction": direction,
            "timeDuration": timeDuration,
            "timeByFrame": int(timeDuration / spriteNumber)
        }
        if isDefault:
            self.defaultAnim = name

    def changeToDefaultAnimation(self):
        """
        Swap to the default animation
        :return:
        """
        self.changeCurrentAnimation(self.defaultAnim)

    def playAnimation(self, deltaTime):
        """
        Calculate new rect
        :param deltaTime:
        :return: Nothing
        """
        animation = self.animeList[self.currentAnim] if self.currentAnim else self.animeList[self.defaultAnim]
        if not animation:
            raise RuntimeError("No animation loaded")

        self.currentTime += deltaTime
        if self.currentTime > animation["timeByFrame"]:
            self.currentTime = 0
            self.currentSprite = (self.currentSprite + 1) % animation["spriteNumber"]
            self.currentRect = pygame.Rect(
                self.imgW * self.currentSprite,
                self.imgH * animation["line"],
                self.imgW,
                self.imgH
            )

    def changeCurrentAnimation(self, name):
        """
        Change the current animation and reset param
        :param name:
        :return: Nothing
        """
        if name == self.currentAnim:
            return

        self.currentAnim = name
        self.currentTime = 0
        self.currentSprite = 0
        self.currentRect = pygame.Rect(
            self.imgW * self.currentSprite,
            self.imgH * self.animeList[name]["line"],
            self.imgW,
            self.imgH
        )