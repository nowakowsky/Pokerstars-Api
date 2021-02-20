import cv2
import numpy as np
from datetime import datetime
from PIL import Image
import pytesseract
import os
import win32gui
import win32ui
from ctypes import windll
try:
    import settings
    import models
except:
    from app import settings
    from app import models



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

def removeScreenshots(screenshots: list):
    for screenshot in screenshots:
        os.remove(screenshot)

def screenshot(windows: list) -> list:
    """
    Takes screenshots and returns list of filenames created

    Credits to hazzey from stackoverflow 
    I've just edited his function to search for windows by partial name and screenshot all of them
    
    https://stackoverflow.com/questions/19695214/python-screenshot-of-inactive-window-printwindow-win32gui
    """
    files = []
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
            files.append(filename)
    return files



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
        __getColor(image))

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
        card = pytesseract.image_to_string(image, config=settings.config_single_word).replace("\f", "").replace("\n", "").replace("\r", "").replace(" ", "")
        if card in '23456789JQKA':
            return card[0]
        elif '10' in card:
            return card[:2]
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

def __checkRed(img):
    red_lower = np.array([136, 87, 111], np.uint8) 
    red_upper = np.array([180, 255, 255], np.uint8) 
    red_mask = cv2.inRange(img, red_lower, red_upper) 
    if len(np.argwhere(red_mask)) > 50:
        return True
        
def __checkGreen(img):  
    green_lower = np.array([25, 52, 72], np.uint8) 
    green_upper = np.array([102, 255, 255], np.uint8) 
    green_mask = cv2.inRange(img, green_lower, green_upper) 
    if len(np.argwhere(green_mask)) > 50:
        return True

def __checkBlue(img):
    blue_lower = np.array([94, 80, 2], np.uint8) 
    blue_upper = np.array([120, 255, 255], np.uint8) 
    blue_mask = cv2.inRange(img, blue_lower, blue_upper)
    if len(np.argwhere(blue_mask)) > 50:
        return True

#more tests to black mask are requied
def __checkBlack(img):
    black_lower = np.array([0, 0, 0], np.uint8) 
    black_upper = np.array([50, 50, 50], np.uint8) 
    black_mask = cv2.inRange(img, black_lower, black_upper) 
    if len(np.argwhere(black_mask)) > 50:
        return True