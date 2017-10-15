import settings.settings as settings

class ScrollManager:
    """

    """

    def __init__(self):
        """
        Not much to do currently
        :return: Nothing
        """
        pass

    def checkPlayerPosition(self, map):
        """
        Checks wether map need to be scrolled
        :param map: map of the game
        :return:
        """

        if map.objects['PLAYER'].x < settings.SCROLL_ZONE:
            map.goToLeft()
        elif map.objects['PLAYER'].x > settings.SCREEN_WIDTH - settings.SCROLL_ZONE:
            map.goToRight()


scrollManager = ScrollManager()

