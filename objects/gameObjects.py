class GameObject:
    '''
    Base class of a game object
    '''

    def __init__(self, name, type, x, y, width, height):
        '''
        Constructor

        '''

        self.name = name
        self.type = type
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Ninja(GameObject):
    """
    A Ninja
    """

    def __init__(self, name, type, x, y, width, height):
        '''
        Constructor

        '''

        super(GameObject, self).__init__(name, type, x, y, width, height)

class Player(GameObject):
    """
    A player
    """

    def __init__(self, name, type, x, y, width, height):
        '''
        Constructor

        '''

        super(GameObject, self).__init__(name, type, x, y, width, height)

class Trap(GameObject):
    """
    A trap
    """

    def __init__(self, name, type, x, y, width, height):
        '''
        Constructor

        '''

        super(GameObject, self).__init__(name, type, x, y, width, height)