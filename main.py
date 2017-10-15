"""
Title: Main File
Desc: Used to start the game
Creation Date: 15/10/17
LastMod Date: 15/10/17
TODO:
* Maybe other transition for menu => loop (especially if we want to return at menu)
"""

from modules.displayManager import displayManager
from modules.inputManager import inputManager
from modules.guiManager import guiManager

def menuLoop():
    while True:
        inputManager.handleMenuEvents()
        if guiManager.startGame:
            break
        guiManager.displayMenu()

def gameLoop():
    while True:
        inputManager.handleEvents()
        displayManager.display()

if __name__ == "__main__":

    displayManager.init()
    menuLoop()
    gameLoop()
    displayManager.quit()
