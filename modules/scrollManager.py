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

        #print('Player pos : ' + str(map.objects['PLAYER'].x) + ' ' + str(map.objects['PLAYER'].y))

        # TODO: To remove
        if map.objects['PLAYER'].x < settings.SCREEN_WIDTH - settings.SCROLL_ZONE_X + 50:
            map.objects['PLAYER'].x += 100

        #if map.objects['PLAYER'].x > settings.SCROLL_ZONE - 50:
        #    map.objects['PLAYER'].x -= 100

        #if map.objects['PLAYER'].x > settings.SCROLL_ZONE_Y - 50:
        #    map.objects['PLAYER'].x -= 100

        #if map.objects['PLAYER'].y < settings.SCREEN_HEIGHT - settings.SCROLL_ZONE_Y + 50:
        #    map.objects['PLAYER'].y += 100

        if map.objects['PLAYER'].x < settings.SCROLL_ZONE_X:
            map.goToLeft()
        elif map.objects['PLAYER'].x > settings.SCREEN_WIDTH - settings.SCROLL_ZONE_X:
            map.goToRight()

        if map.objects['PLAYER'].y < settings.SCROLL_ZONE_Y:
            map.goUp()
        elif map.objects['PLAYER'].y > settings.SCREEN_HEIGHT - settings.SCROLL_ZONE_Y:
            map.goDown()


scrollManager = ScrollManager()

