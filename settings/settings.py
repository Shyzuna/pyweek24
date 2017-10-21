import os

# Path
MAPS_PATH = os.path.join('data', 'maps')
IMGS_PATH = os.path.join('data', 'imgs')
TILES_PATH = os.path.join(IMGS_PATH, 'tiles')
BG_PATH = os.path.join(IMGS_PATH, 'background')
MENU_PATH = os.path.join(IMGS_PATH, 'menu')
OBJECTS_PATH = os.path.join(IMGS_PATH, 'objects')
CHARACTERS_PATH = os.path.join(IMGS_PATH, 'characters')
TRAPS_PATH = os.path.join(IMGS_PATH, 'traps')
HUD_PATH = os.path.join(IMGS_PATH, 'hud')
FONTS_PATH = os.path.join('data', 'fonts')
DIALOGS_PATH = os.path.join('data', 'dialogs')
END_SCREEN_PATH = os.path.join('data', 'imgs', 'screens', 'victory.png')
SOUNDS_PATH = os.path.join('data', 'sounds')

# Display
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_PLAYING_HEIGHT = 700
FPS = 60

# Scroll zone (in pixels)
SCROLL_ZONE_X = 400
SCROLL_ZONE_Y = 250
# Scroll speed
SCROLL_SPEED = 1

# Important
GAME_TITLE = "Beyond the game"

# Other
DATA_DELIMITER = '------'

MAX_VELOCITY_X = 300
MAX_VELOCITY_Y = 300

PLAYER_ID = 'player1'

INTRO_DIALOG_ID = '1'
END_DIALOG_ID = '7'