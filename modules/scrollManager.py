"""
Title: scrollManager File
Desc: Manage all the scrolling stuff
Creation Date: 15/10/17
LastMod Date: 15/10/17
TODO:
*
"""

import settings.settings as settings
from objects.enums import ObjectName

class ScrollManager:
    """
    Handle scrolling of the map if player is in the scrolling zones
    """

    def __init__(self):
        """
        Not much to do currently
        :return: Nothing
        """
        pass

    def isScrollNeeded(self, mapManager, player, distX, distY):
        """
        Calculate if we need to scroll the map
        :param mapManager:
        :param player:
        :param distX:
        :param distY:
        :return: (distX,distY) if we need else None
        """
        playerX = player.x + distX
        playerY = player.y + distY

        scrollX = 0
        scrollY = 0

        # TODO: Scrolling zone in percent ? param in settings or not ?

        # Check if char in horizontal scrolling zone
        if playerX < settings.SCROLL_ZONE_X:
            # To avoid oposite scrolling bug
            scrollX = -1 * abs(distX)
        elif playerX > settings.SCREEN_WIDTH - settings.SCROLL_ZONE_X:
            scrollX = abs(distX)

        # Check if char in vertical scrolling zone
        if playerY < settings.SCROLL_ZONE_Y:
            # To avoid oposite scrolling bug
            scrollY = -1 * abs(distY)
        elif playerY > settings.SCREEN_PLAYING_HEIGHT - settings.SCROLL_ZONE_Y:
            scrollY = abs(distY)

        # Check if overextend map values
        if (mapManager.currentRect.x + distX) < 0:
            distX = -1 * mapManager.currentRect.x
        elif (mapManager.currentRect.x + distX) > (mapManager.mapSizeX - settings.SCREEN_WIDTH):
            distX = (mapManager.mapSizeX - settings.SCREEN_WIDTH) - mapManager.currentRect.x
        if (mapManager.currentRect.y + distY) < 0:
            distY = mapManager.currentRect.y
        elif (mapManager.currentRect.y + distY) > (mapManager.mapSizeY - settings.SCREEN_PLAYING_HEIGHT):
            distY = (mapManager.mapSizeY - settings.SCREEN_PLAYING_HEIGHT) - mapManager.currentRect.y

        if scrollX == 0 and scrollY == 0:
            return 0
        else:
            return scrollX,scrollY

scrollManager = ScrollManager()

