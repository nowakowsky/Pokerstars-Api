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

    def readData(self, screenshot):
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

class MultiBot:
    # this will be changed soon
    handlers = []
    bots = []
    gameWindows = []
    def __init__(self):
        self.gameWindows = tools.moveAndResizeWindows()
        screenshots = tools.grabScreen(self.gameWindows)
        activeTables = [x.tableName for x in screenshots]

        for table in activeTables:
            # init bot
            bot = PokerBot()
            bot.tableName = table
            
            # init handler
            changesHandler = ChangesHandler(bot)
            
            # list bots and handlers
            self.handlers.append(changesHandler)
            self.bots.append(bot)

    def run(self):
        while 1:
            # this can help if user moves window, not sure if needed
            #gameWindows = tools.moveAndResizeWindows()

            screenshots = tools.grabScreen(self.gameWindows)
            activeTables = [x.tableName for x in screenshots]
            
            for screenshot in screenshots:
                bot = next(filter(lambda b: b.tableName == screenshot.tableName, self.bots))
                handler = next(filter(lambda h: h.tableName == screenshot.tableName, self.handlers))

                bot.readData(screenshot)
                handler.check(bot)