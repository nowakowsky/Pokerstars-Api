# This app reads data from PokerStars game.
### It can work on any number of tables simultaneously

PokerStars windows don't even have to be visible, but **cannot be minimalized**.


At the moment this app recons:
* Cards on table
* Player cards
* Game stage

** To make it work you need to set up orange table and default deck with 4 colors! **

Letter "X" and "?" signs means that card wasn't recognized properly.

# Example output
```
########################
Player cards [T9, C6]
Cards on table: [TA, H6, H4, CJ, C5]
Game state: River
Table: Gotha VI
########################
Player cards [T2, C6]
Cards on table: []
Game state: Prefloop
Table: Aida VI
########################
Player cards []
Cards on table: [HQ, P8, C2]
Game state: Floop
Table: Aitne VI
########################
```
## This is just a side project to learn some programming basics written in few hours, do not expect too much. Anyway it is working pretty good
### This is not completed app, treat it as a beta version 
 
### It uses tesseract, opencv, pywin32, numpy and Pillow
[Get tesseract installer](https://github.com/UB-Mannheim/tesseract/wiki)
I was using tesseract-ocr-w64-setup-v5.0.0-alpha.20201127

[Above url is listed on official tesseract readme](https://github.com/tesseract-ocr/tesseract)

[Tesseract wrapper docs](https://pypi.org/project/pytesseract/)
