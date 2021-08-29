from browser import document, html

# debug
debug = document["debugarea"]
def msg (s):
    debug.text = str(s)

# Size and position
STONE_SIZE = 32
NR_ROW = 12
NR_COLUMN = 6
FIELD_WIDTH = NR_COLUMN * STONE_SIZE
FIELD_HEIGHT = NR_ROW * STONE_SIZE

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

    def draw (self):
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

    def fall (self, column_ids = range(NR_COLUMN)):
        for column_id in column_ids:
            for row_id in range(NR_ROW - 1, 0, -1):
                msg(row_id)
                if self.field[row_id][column_id] == None and self.field[row_id - 1][column_id] != None:
                    self.field[row_id][column_id] = self.field[row_id - 1][column_id]
                    self.field[row_id - 1][column_id] = None

    def clear (self):
        self.field = [[None] * NR_COLUMN for i in range(NR_ROW)]

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
field.field[0][0] = 0
field.field[0][1] = 1
field.field[1][2] = 2
field.field[2][2] = 3

def cursol (event):
    if event.charCode == CHARCODE_UP:
        pass
    elif event.charCode == CHARCODE_DOWN:
        pass
    elif event.charCode == CHARCODE_RIGHT:
        pass
    elif event.charCode == CHARCODE_LEFT:
        pass
    elif event.charCode == CHARCODE_SPACE:
        pass
    field.fall()
    field.draw()

document.bind("keypress", cursol)
