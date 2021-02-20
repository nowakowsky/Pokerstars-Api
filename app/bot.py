import tools
import os
import models

class PokerBot:
    gameWindows = []

    def __init__():
        self.gameWindows = tools.moveAndResizeWindows()

    def __checkGameState() -> str:
        if not len(self.tableCards):
            return "Prefloop"
        elif len(self.tableCards) == 4:
            return "Turn"
        elif len(self.tableCards) == 5:
            return "River"
        else:
            return "Floop"

    def readData():
        screenshots = tools.screenshot()

        for screenshot in screenshots:
            #read player cards
            self.playerCards = None
            #read table cards
            self.tableCards = None
            #read game state
            self.gameState = __checkGameState()

        tools.removeScreenshots()
