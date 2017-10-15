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

if __name__ == "__main__":
    mapManager.load('test.map', [])
    displayManager.init()
    while True:
        inputManager.handleEvents()
    displayManager.quit()