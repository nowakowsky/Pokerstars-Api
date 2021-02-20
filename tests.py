
import cv2
from app import tools
from os import listdir
from os.path import isfile, join

import unittest
class TestCases(unittest.TestCase):
    def test_color_recon(self):
        images = ["serce.png", "dupa.png", "zol.png", "diament.png"]
        colors = ["Heart", "Pike", "Clover", "Tile"]
        path = "tests_imgs"

        for image, expected in zip(images, colors):
            img = cv2.imread(path + '\\' + image)
            self.assertEqual(tools.__getCardColor(img), expected)

    def test_card_recon(self):
        cards_path = "tests_imgs\\cards\\"
        images = [f for f in listdir(cards_path) if isfile(join(cards_path, f))]
        
        for image in images:
            img = cv2.imread(cards_path + "\\" + image, 0)
            self.assertEqual(tools.__getCardValue(img), image.replace(".png", ""))

if __name__ == '__main__':
    unittest.main()