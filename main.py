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

if __name__ == "__main__":
    displayManager.init()
    while True:
        inputManager.handleEvents()
    displayManager.quit()