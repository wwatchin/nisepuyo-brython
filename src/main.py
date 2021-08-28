from browser import document, html
import math
import random

canvas = document["drawarea"]
context = canvas.getContext("2d")

x = 10
y = 5

# Images
images_stone = (html.IMG(src="img/stone1.png"), html.IMG(src="img/stone2.png"),
                html.IMG(src="img/stone3.png"), html.IMG(src="img/stone4.png"),
                html.IMG(src="img/stone5.png"))
# WASD
CHARCODE_UP = 119
CHARCODE_LEFT = 97
CHARCODE_DOWN = 115
CHARCODE_RIGHT = 100
CHARCODE_SPACE = 32

def draw ():
    context.clearRect(0, 0, 800, 640)
    context.drawImage(images_stone[0], x, y)

def cursol (event):
    global x
    global y
    if event.charCode == CHARCODE_UP:
        y -= 1
    elif event.charCode == CHARCODE_DOWN:
        y += 1
    elif event.charCode == CHARCODE_RIGHT:
        x += 1
    elif event.charCode == CHARCODE_LEFT:
        x -= 1
    elif event.charCode == CHARCODE_SPACE:
        x = 0
        y = 0
    draw()

document.bind("keypress", cursol)
