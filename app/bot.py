import tools
import os
import models
import cv2
class PokerBot:
    gameWindows = []
    def __init__(self):
        self.gameWindows = tools.moveAndResizeWindows()
        self.tableCards = []

    def __checkGameState(self) -> str:
        if not len(self.tableCards):
            return "Prefloop"
        elif len(self.tableCards) == 4:
            return "Turn"
        elif len(self.tableCards) == 5:
            return "River"
        else:
            return "Floop"

    def readData(self):
        screenshots = tools.screenshot(self.gameWindows)
        for screenshot in screenshots:
            self.tableCards = tools.readTableCards(screenshot)
            print (*self.tableCards)
            # for each in
        # for screenshot in screenshots:
        #     #read player cards
        #     self.playerCards = None
        #     #read table cards
        #     self.tableCards = None
        #     #read game state
        #     self.gameState = __checkGameState()

        #tools.removeScreenshots()

    
import time

if __name__ == "__main__":
    while 1:
        bot = PokerBot()
        bot.readData()
        print ("###")
        time.sleep(2)