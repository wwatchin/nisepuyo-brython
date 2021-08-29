from browser import document, html

# debug
debug = document["debugarea"]
def msg (s):
    debug.text = str(s)

# Size and position
STONE_SIZE = 32
NR_ROW = 6
NR_COLUMN = 12
FIELD_WIDTH = NR_ROW * STONE_SIZE
FIELD_HEIGHT = NR_COLUMN * STONE_SIZE

# WASD + SPACE
CHARCODE_UP = 119
CHARCODE_LEFT = 97
CHARCODE_DOWN = 115
CHARCODE_RIGHT = 100
CHARCODE_SPACE = 32

# Field
class Field ():
    def __init__ (self, context, images_stone, posx = 0, posy = 0):
        self.__x = posx
        self.__y = posy
        self.__endx = posx + FIELD_WIDTH
        self.__endy = posy + FIELD_HEIGHT
        self.__context = context
        self.__images_stone = images_stone
        self.clear()

    def draw(self):
        self.__context.clearRect(self.__x, self.__y, self.__endx, self.__endy)
        y = self.__y
        for row in self.field:
            x = self.__x
            for cell in row:
                if cell != None:
                    self.__context.drawImage(self.__images_stone[cell], x, y)
                x += STONE_SIZE
            y += STONE_SIZE
        msg(self.field)

    def clear(self):
        self.field = [[None] * NR_ROW for i in range(NR_COLUMN)]

###
### Materials.
###
images_stone = (html.IMG(src="img/stone0.png"), html.IMG(src="img/stone1.png"),
                html.IMG(src="img/stone2.png"), html.IMG(src="img/stone3.png"),
                html.IMG(src="img/stone4.png"), html.IMG(src="img/stone5.png"))

###
### Main routine.
###
canvas = document["drawarea"]
context = canvas.getContext("2d")
field = Field(context, images_stone)

def cursol (event):
    debug.text = "a"
    if event.charCode == CHARCODE_UP:
        field.field[0][0] = 0
        pass
    elif event.charCode == CHARCODE_DOWN:
        field.field[1][0] = 1
        pass
    elif event.charCode == CHARCODE_RIGHT:
        field.field[1][1] = 2
        pass
    elif event.charCode == CHARCODE_LEFT:
        field.field[1][2] = 3
        pass
    elif event.charCode == CHARCODE_SPACE:
        field.field[2][2] = 4
        pass
    field.draw()

document.bind("keypress", cursol)