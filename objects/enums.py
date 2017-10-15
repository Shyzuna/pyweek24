"""
Title: colors File
Desc: Colors enumeration
Creation Date: 15/10/17
LastMod Date: 15/10/17
TODO:
*
"""

from enum import Enum

class Colors(Enum):
    BLACK = (0,0,0)
    WHITE = (255,255,255)

class ObjectName(Enum):
    """
    Enum for object names
    """

    BOX = 'BOX'
    WALL = 'WALL'
    LADDER = 'LADDER'
    BALL = 'BALL'
    SPIKES = 'SPIKES'
    SAW = 'SAW'
    ACID = 'ACID'
    NINJA = 'NINJA'
    PLAYER = 'PLAYER'

class ObjectType(Enum):
    """
    Enum for object types
    """

    GAME_OBJECT = 'GAMEOBJECT'
    NINJA = 'NINJA'
    PLAYER = 'PLAYER'
    TRAP = 'TRAP'
