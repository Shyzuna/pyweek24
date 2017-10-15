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
from modules.mapManager import mapManager
from modules.scrollManager import scrollManager

def menuLoop():
    while True:
        inputManager.handleMenuEvents(guiManager)
        if guiManager.startGame:
            break
        guiManager.displayMenu()

def gameLoop():
    while True:
        # TODO: Test si l'on est en mouvement pour éviter de lancer pour rien
        scrollManager.checkPlayerPosition(mapManager)

        inputManager.handleEvents()
        displayManager.display()

if __name__ == "__main__":
    displayManager.init()
    guiManager.init()
    mapManager.load('test.map',[])
    menuLoop()
    gameLoop()
    displayManager.quit()
