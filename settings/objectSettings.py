from objects.enums import ObjectName
import os
import settings.settings as settings

objectProperties = {
    ObjectName.BOX: {
        'isThrowable': False,
        'isMovable': True,
        'isClimbable': False,
        'imgPath': os.path.join(settings.OBJECTS_PATH, "box.png"),
        'imgRatio': 2
    },
    ObjectName.WALL: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    ObjectName.LADDER: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': True
    },
    ObjectName.BALL: {
        'isThrowable': True,
        'isMovable': False,
        'isClimbable': False
    },
    ObjectName.SPIKES: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    ObjectName.SAW: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    ObjectName.ACID: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    ObjectName.NINJA: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False,
        'imgPath': os.path.join(settings.CHARACTERS_PATH, "Ninja.png"),
        'imgRatio': 1
    },
    ObjectName.PLAYER: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False,
        'imgPath': os.path.join(settings.CHARACTERS_PATH, "Player.png"),
        'imgRatio': 1
    }
}