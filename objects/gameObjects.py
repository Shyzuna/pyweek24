
import os
import settings.settings as settings

class GameObject:
    '''
    Base class of a game object
    '''

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.tileX = tileX
        self.tileY = tileY
        self.width = width
        self.height = height


class Ninja(GameObject):
    """
    A Ninja
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        super(Ninja, self).__init__(name, type, x, y, tileX, tileY, width, height)

class Player(GameObject):
    """
    A player
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        super(Player, self).__init__(name, type, x, y, tileX, tileY, width, height)

class Trap(GameObject):
    """
    A trap
    """

    def __init__(self, name, type, x, y, tileX, tileY, width, height):
        '''
        Constructor

        '''

        super(Trap, self).__init__(name, type, x, y, tileX, tileY, width, height)