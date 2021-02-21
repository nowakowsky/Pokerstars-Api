import tools
import os
import models
import cv2
import threading

class PokerBot:
    gameState = ""
    playerCards = []
    tableCards = []
    tableName = ""

    def checkGameState(self) -> str:
        if not len(self.tableCards):
            return "Prefloop"
        elif len(self.tableCards) == 4:
            return "Turn"
        elif len(self.tableCards) == 5:
            return "River"
        else:
            return "Floop"

    def readData(self):
        self.tableCards = tools.readTableCards(screenshot.filename)
        self.playerCards = tools.readPlayerCards(screenshot.filename)
        self.gameState = self.checkGameState()
        

class ChangesHandler:
    tableName = ""
    def __init__(self, bot: PokerBot):
        self.gameState = bot.gameState
        self.playerCards = bot.playerCards
        self.tableCards = bot.tableCards
        self.tableName = bot.tableName
    
    def check(self, bot: PokerBot):
        if self.gameState != bot.gameState or self.playerCards != bot.playerCards or self.tableCards != bot.tableCards:
            self.gameState = bot.gameState
            self.playerCards = bot.playerCards
            self.tableCards = bot.tableCards
            self.printData()

        
    def printData(self):
        print (f'Player cards {self.playerCards}')
        print (f'Cards on table: {self.tableCards}')
        print (f'Game state: {self.gameState}')
        print (f'Table: {self.tableName}')
        print ("########################")

import time

if __name__ == "__main__":
    handlers = []
    bots = []
    gameWindows = tools.moveAndResizeWindows()
    while 1:
        screenshots = tools.grabScreen(gameWindows)
        activeTables = [x.tableName for x in screenshots]
        
        # first run
        if handlers == []:
            for table in activeTables:
                # init bot
                bot = PokerBot()
                bot.tableName = table
                
                # init handler
                changesHandler = ChangesHandler(bot)
                
                # create lists
                handlers.append(changesHandler)
                bots.append(bot)

        for screenshot in screenshots:
            bot = next(filter(lambda b: b.tableName == screenshot.tableName, bots))
            handler = next(filter(lambda h: h.tableName == screenshot.tableName, handlers))

            bot.readData()
            handler.check(bot)

    # for screenshot in screenshots:
    #     changesHandler = ChangesHandler(self)
    #     self.tableCards = tools.readTableCards(screenshot.filename)
    #     self.playerCards = tools.readPlayerCards(screenshot.filename)
    #     self.gameState = self.checkGameState()
    #     changesHandler.check(self)
    #     del changesHandler


    #     bot = PokerBot()
    #     bot.readData()
    #     print ("###")
    #     time.sleep(2)