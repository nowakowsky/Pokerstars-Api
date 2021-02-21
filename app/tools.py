import cv2
import numpy as np
from datetime import datetime
from PIL import Image
import pytesseract
import os
import win32gui
import win32ui
from ctypes import windll
import settings
import models



def readPlayerCards(filename: str) -> list:
    cards = []

    cards_diff = 37
    card1 = [285, 296, 298, 312]
    card2 = [285+cards_diff, 296+cards_diff, 298, 312]

    image = cv2.imread(filename)
    # image = cv2.imread("105255_095302.png")

    card1 = image[card1[2]:card1[3], card1[0]:card1[1]]
    card2 = image[card2[2]:card2[3], card2[0]:card2[1]]

    # if card not on table yet
    if emptyCard(card2):
        pass
    else:
        cards.append(cardInfo(card1))
        cards.append(cardInfo(card2))

    return cards

def readTableCards(filename: str) -> list:
    cards = []

    # y position for cards on table don't change
    cards_y1, cards_y2 = 174, 190

    # x changes by 39 px right
    cards_diff = 39
    
    # hardcoded card 1 x position
    table_cards = [226, 237]

    # hardcoded floop, turn and river positions
    for i in range(1,5):
        table_cards.append(table_cards[0] + cards_diff * i)
        table_cards.append(table_cards[1] + cards_diff * i)

    image = cv2.imread(filename)
    
    for i in range(0,10,2):
        #that can be improved, card "10" has other coords
        if i == 6 or i == 4:
            card = image[cards_y1:cards_y2, table_cards[i]-2:table_cards[i+1]]
        elif i == 8:
            card = image[cards_y1:cards_y2, table_cards[i]-2:table_cards[i+1]-3]
        else:
            card = image[cards_y1:cards_y2, table_cards[i]:table_cards[i+1]]

        # if card not on table yet
        if not emptyCard(card):
            cards.append(cardInfo(card))

    return cards


def emptyCard(img) -> bool:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    orange_lower = np.array([10, 100, 20], np.uint8) 
    orange_upper = np.array([25, 255, 255], np.uint8)
    orange_mask = cv2.inRange(img, orange_lower, orange_upper) 
    if len(np.argwhere(orange_mask)) > 100:
        return True

pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path

def __searchHwnds(name: str) -> list:
    """
    Searches for windows by partial name and returns list of hwnd
    """
    hwnds = []
    def foreach_window(hwnd, lParam):
        if name in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)
    win32gui.EnumWindows(foreach_window, None)
    return hwnds

def grabScreen(windows: list) -> list:
    """
    Takes screenshots and returns list of models.Screenshot objects

    Credits to hazzey from stackoverflow 
    I've just edited his function to search for windows by partial name, screenshot all of them and grab table name
    
    https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
    """
    screenshots = []
    for hwnd in windows:
        left, top, right, bot = win32gui.GetWindowRect(hwnd)
        w = right - left
        h = bot - top
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

        saveDC.SelectObject(saveBitMap)

        result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)

        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        if result == 1:
            filename = datetime.now().strftime("%H%M%S_%f") + '.png'
            im.save(filename)
            tablename = win32gui.GetWindowText(hwnd).split("-")[0]
            screenshot = models.Screenshot(tablename, filename)
            screenshots.append(screenshot)
    return screenshots



def moveAndResizeWindows() -> list:
    """
    this function prepares windows, it can be easly changed if anything will require visibility
    returns output of __searchHwnds (all found hwnds)
    """
    name = "Limit" # partial window name

    game_window = [0,0,640,540]
    game_windows = __searchHwnds(name)
    for hwnd in game_windows:
        win32gui.MoveWindow(hwnd, *game_window, True)
    return game_windows

def cardInfo(image) -> models.Card:
    """
    Calls __getCardValue and __getCardColor and returns Card object
    """
    card = models.Card(__getCardValue(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)),
        __getCardColor(image))

    return card

def __getCardValue(image) -> str:
    """
    Do not use, it's is being called by cardInfo()
    
    Takes an image and returns card as a string:
        -> 2
        -> ...
        -> A
        -> X - error

    Uses --pcm 7 and --pcm 9 if first one fails
    Tested on grayscale images, more tests are requied.
    """
    card = pytesseract.image_to_string(image, config=settings.config_single_line).replace("\f", "").replace("\n", "").replace("\r", "").replace(" ", "")
    try:
        if card in '23456789JQKA':
            return card[0]
        elif '10' in card:
            return card[:2]
    except:
        try:
            card = pytesseract.image_to_string(image, config=settings.config_single_word).replace("\f", "").replace("\n", "").replace("\r", "").replace(" ", "")
            if card in '23456789JQKA':
                return card[0]
            elif '10' in card:
                return card[:2]
        except:
            return "?"
    return "X"

def __getCardColor(image) -> models.Colors:
    """
    Do not use, it's is being called by cardInfo()

    Takes an image in BGR format an returns a string:
        -> Tile
        -> Heart 
        -> Clover
        -> Pike
        -> Error
    """
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) 
    if __checkBlue(image):
        return models.Colors.Tiles
    elif __checkRed(image):
        return models.Colors.Hearts
    elif __checkGreen(image):
        return models.Colors.Clovers
    elif __checkBlack(image):
        return models.Colors.Pikes
    return models.Colors.Error

def __checkRed(img) -> bool:
    red_lower = np.array([136, 87, 111], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
    red_mask = cv2.inRange(img, red_lower, red_upper) 
    if len(np.argwhere(red_mask)) > 30:
        return True
        
def __checkGreen(img) -> bool:  
    green_lower = np.array([25, 52, 72], np.uint8) 
    green_upper = np.array([102, 255, 255], np.uint8) 
    green_mask = cv2.inRange(img, green_lower, green_upper) 
    if len(np.argwhere(green_mask)) > 30:
        return True

def __checkBlue(img) -> bool:
    blue_lower = np.array([94, 80, 2], np.uint8) 
    blue_upper = np.array([120, 255, 255], np.uint8) 
    blue_mask = cv2.inRange(img, blue_lower, blue_upper)
    if len(np.argwhere(blue_mask)) > 30:
        return True

#more tests to black mask are requied
def __checkBlack(img) -> bool:
    black_lower = np.array([0, 0, 0], np.uint8) 
    black_upper = np.array([50, 50, 50], np.uint8) 
    black_mask = cv2.inRange(img, black_lower, black_upper) 
    if len(np.argwhere(black_mask)) > 20:
        return True

