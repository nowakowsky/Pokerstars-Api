import tools
import models
import os
import cv2
import threading

class PokerBot:
    gameState = ""
    playerCards = []
    tableCards = []
    # tableName = ""

    def checkGameState(self) -> str:
        if not len(self.tableCards):
            return "Prefloop"
        elif len(self.tableCards) == 4:
            return "Turn"
        elif len(self.tableCards) == 5:
            return "River"
        else:
            return "Floop"

    def readData(self, screenshot):
        self.tableCards = tools.readTableCards(screenshot.filename)
        self.playerCards = tools.readPlayerCards(screenshot.filename)
        self.gameState = self.checkGameState()
        

class ChangesHandler:
    tableName = ""
    def __init__(self, bot: PokerBot, tableName: str):
        self.gameState = bot.gameState
        self.playerCards = bot.playerCards
        self.tableCards = bot.tableCards
        self.tableName = tableName
    
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

class MultiBot:
    bot_dict = {}
    def __init__(self):
        self.gameWindows = tools.moveAndResizeWindows()
        screenshots = tools.grabScreen(self.gameWindows)

        for img in screenshots:
            bot = PokerBot()
            img.tableName

            changesHandler = ChangesHandler(bot, img.tableName)
            self.bot_dict[img.tableName] = [bot, changesHandler]
    
    def run(self):
        while 1:
            screenshots = tools.grabScreen(self.gameWindows)
            for img in screenshots:
                bot, changesHandler = self.bot_dict[img.tableName]
                bot.readData(img)
                changesHandler.check(bot)