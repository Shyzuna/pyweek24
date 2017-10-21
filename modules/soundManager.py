import pygame
import os

import settings.settings as settings

class SoundManager:

    def __init__(self):
        pass


    def init(self):
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(settings.SOUNDS_PATH, 'main.mp3'))
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

soundManager = SoundManager()