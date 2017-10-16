import settings.settings as settings
from objects.enums import ObjectName

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

        #print('Player pos : ' + str(map.objects[ObjectName.PLAYER].x) + ' ' + str(map.objects[ObjectName.PLAYER].y))

        # TODO: To remove
        if map.objects[ObjectName.PLAYER].x < settings.SCREEN_WIDTH - settings.SCROLL_ZONE_X + 50:
            map.objects[ObjectName.PLAYER].x += 100

        #if map.objects[ObjectName.PLAYER].x > settings.SCROLL_ZONE - 50:
        #    map.objects[ObjectName.PLAYER].x -= 100

        #if map.objects[ObjectName.PLAYER].x > settings.SCROLL_ZONE_Y - 50:
        #    map.objects[ObjectName.PLAYER].x -= 100

        #if map.objects[ObjectName.PLAYER].y < settings.SCREEN_HEIGHT - settings.SCROLL_ZONE_Y + 50:
        #    map.objects[ObjectName.PLAYER].y += 100

        if map.objects[ObjectName.PLAYER].x < settings.SCROLL_ZONE_X:
            map.goToLeft()
        elif map.objects[ObjectName.PLAYER].x > settings.SCREEN_WIDTH - settings.SCROLL_ZONE_X:
            map.goToRight()

        if map.objects[ObjectName.PLAYER].y < settings.SCROLL_ZONE_Y:
            map.goUp()
        elif map.objects[ObjectName.PLAYER].y > settings.SCREEN_HEIGHT - settings.SCROLL_ZONE_Y:
            map.goDown()


scrollManager = ScrollManager()

