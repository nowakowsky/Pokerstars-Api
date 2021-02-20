
import pytesseract
import settings
import cv2
import tools


pytesseract.pytesseract.tesseract_cmd = settings.tesseract_path

a = tools.cardInfo(cv2.imread("9.png"))
b = tools.cardInfo(cv2.imread("9b.png"))
c = tools.cardInfo(cv2.imread("10r.png"))

print (a, b, c)
### cards recon test
# from os import listdir
# from os.path import isfile, join

# cards_path = "..\\tests_imgs\\cards\\"
# images = [f for f in listdir(cards_path) if isfile(join(cards_path, f))]
# print (images)
# for image in images:
#     img = cv2.imread(cards_path + "\\" + image, 0)
#     print(tools.getCard(img))
#     # tools.getCard(img)


### color recon test
# images = ["serce.png", "dupa.png", "zol.png", "diament.png"]
# for image in images:
#     card_color = tools.getColor(cv2.imread(image))
#     print (f'Card color for {image} is {card_color}')


### shitcodes
# print(pytesseract.image_to_string(img_cv, config=config_single_line))

# img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
# img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
# img_bw = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY)[1]
# cv2.imshow("a", img_bw)
# cv2.imwrite(r'img.png', img_bw)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# print(pytesseract.image_to_string(img_cv, config=config_single_line))
# print(pytesseract.image_to_string(img_gray))
# --psm 7 --oem 3 -c tessedit_char_whitelist=/1234

# print(pytesseract.image_to_string(Image.open(r'image.png'), lang="eng"))
