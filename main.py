"""
Title: Main File
Desc: Used to start the game
Creation Date: 15/10/17
LastMod Date: 15/10/17
TODO:
*
"""

from modules.displayManager import displayManager
from modules.inputManager import inputManager
from modules.mapManager import mapManager
from modules.scrollManager import scrollManager

if __name__ == "__main__":
    mapManager.load('test.map', [])
    displayManager.init()
    while True:
        # TODO: Test si l'on est en mouvement pour éviter de lancer pour rien
        scrollManager.checkPlayerPosition(mapManager)

        inputManager.handleEvents()
    displayManager.quit()