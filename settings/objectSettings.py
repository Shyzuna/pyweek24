from objects.enums import ObjectName as objectType

objectProperties = {
    objectType.BOX: {
        'isThrowable': False,
        'isMovable': True,
        'isClimbable': False
    },
    objectType.WALL: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    objectType.LADDER: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': True
    },
    objectType.BALL: {
        'isThrowable': True,
        'isMovable': False,
        'isClimbable': False
    },
    objectType.SPIKES: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    objectType.SAW: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    objectType.ACID: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    objectType.NINJA: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    },
    objectType.NINJA: {
        'isThrowable': False,
        'isMovable': False,
        'isClimbable': False
    }
}