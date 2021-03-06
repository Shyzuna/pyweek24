from objects.enums import ObjectName,Direction,AnimationType

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

ObjectsAnimations = {
    ObjectName.PLAYER: {
        'imgPath': os.path.join(settings.CHARACTERS_PATH, "Player.png"),
        'maxSpriteW': 5,
        'maxSpriteH': 5,
        'imgRatio': 1,
        'animations': [
            {
                "name": AnimationType.WALKING,
                "direction": Direction.RIGHT,
                "spriteNumber": 5,
                "line": 0,
                "isDefault": False,
                "timeDuration": 800
            },
            {
                "name": AnimationType.IDLE,
                "direction": Direction.RIGHT,
                "spriteNumber": 2,
                "line": 2,
                "isDefault": True,
                "timeDuration": 1000
            },
            {
                "name": AnimationType.DEAD,
                "direction": Direction.RIGHT,
                "spriteNumber": 2,
                "line": 3,
                "isDefault": False,
                "timeDuration": 1000
            }
        ]
    },
    ObjectName.BOX: {
        'imgPath': os.path.join(settings.OBJECTS_PATH, "box.png"),
        'maxSpriteW': 1,
        'maxSpriteH': 1,
        'imgRatio': 2.2,
        'animations': [
            {
                "name": AnimationType.IDLE,
                "direction": Direction.RIGHT,
                "spriteNumber": 1,
                "line": 0,
                "isDefault": True,
                "timeDuration": -1
            }
        ]
    },
    ObjectName.SPIKES: {
        'imgPath': os.path.join(settings.TRAPS_PATH, "c.png"),
        'maxSpriteW': 1,
        'maxSpriteH': 1,
        'imgRatio': 2.4,
        'animations': [
            {
                "name": AnimationType.IDLE,
                "direction": Direction.RIGHT,
                "spriteNumber": 1,
                "line": 0,
                "isDefault": True,
                "timeDuration": -1
            }
        ]
    },
    ObjectName.ACID: {
        'imgPath': os.path.join(settings.TRAPS_PATH, "a.png"),
        'maxSpriteW': 1,
        'maxSpriteH': 1,
        'imgRatio': 2,
        'animations': [
            {
                "name": AnimationType.IDLE,
                "direction": Direction.RIGHT,
                "spriteNumber": 1,
                "line": 0,
                "isDefault": True,
                "timeDuration": -1
            }
        ]
    },
    ObjectName.NINJA: {
        'imgPath': os.path.join(settings.CHARACTERS_PATH, "Ninja.png"),
        'maxSpriteW': 5,
        'maxSpriteH': 5,
        'imgRatio': 1,
        'animations': [
            {
                "name": AnimationType.IDLE,
                "direction": Direction.RIGHT,
                "spriteNumber": 2,
                "line": 2,
                "isDefault": True,
                "timeDuration": 1000
            }
        ]
    },
    ObjectName.SAW: {
        'imgPath': os.path.join(settings.TRAPS_PATH, "b.png"),
        'maxSpriteW': 1,
        'maxSpriteH': 1,
        'imgRatio': 2.8,
        'animations': [
            {
                "name": AnimationType.IDLE,
                "direction": Direction.RIGHT,
                "spriteNumber": 1,
                "line": 0,
                "isDefault": True,
                "timeDuration": -1
            }
        ]
    }
}