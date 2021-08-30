from browser import document
from browser import html
from browser import timer
import random

# debug
debug = document["debugarea"]
def msg (s):
    debug.text = str(s)

# Literals
STONE_SIZE = 32
NR_ROW = 12
NR_COLUMN = 6
FIELD_WIDTH = NR_COLUMN * STONE_SIZE
FIELD_HEIGHT = NR_ROW * STONE_SIZE
POSX_NEWSTONE = 2
POSY_NEWSTONE = 1
DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_LEFT = range(4)
POS_PAIRSTONE = ((0, -1), (1, 0), (0, 1), (-1, 0))
TIMER_TICK = 100

# WASD + SPACE
CHARCODE_UP = 119
CHARCODE_LEFT = 97
CHARCODE_DOWN = 115
CHARCODE_RIGHT = 100
CHARCODE_SPACE = 32

# Field
class Field ():
    def __init__ (self, context, images_stone, posx = 0, posy = 0, period = 5):
        self.__x = posx
        self.__y = posy
        self.__endx = posx + FIELD_WIDTH
        self.__endy = posy + FIELD_HEIGHT
        self.__context = context
        self.__images_stone = images_stone
        self.__nr_stones = len(images_stone) - 1
        self.__cursorx = None
        self.__cursory = None
        self.__direction = None
        self.__fall_period = period
        self.reset_counter()
        self.clear()

    def __get_pair_position (self):
        return (self.__cursorx + POS_PAIRSTONE[self.__direction][0],
                self.__cursory + POS_PAIRSTONE[self.__direction][1])

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

    def newstone (self):
        self.__cursorx = POSX_NEWSTONE
        self.__cursory = POSY_NEWSTONE
        self.__direction = DIRECTION_UP
        self.field[POSY_NEWSTONE-1][POSX_NEWSTONE] = random.randint(1, self.__nr_stones)
        self.field[POSY_NEWSTONE][POSX_NEWSTONE] = random.randint(1, self.__nr_stones)

    def move_left (self):
        pairx, pairy = self.__get_pair_position()
        if pairx == 0 or self.__cursorx == 0:
            return
        if self.field[pairy][pairx - 1] != None and pairx - 1 != self.__cursorx:
            return
        if self.field[self.__cursory][self.__cursorx - 1] and self.__cursorx - 1 != pairx:
            return
        cur, pair = self.field[self.__cursory][self.__cursorx], self.field[pairy][pairx]
        self.field[pairy][pairx] = None
        self.field[self.__cursory][self.__cursorx] = None
        self.field[pairy][pairx - 1] = pair
        self.field[self.__cursory][self.__cursorx - 1] = cur
        self.__cursorx -= 1

    def move_right (self):
        pairx, pairy = self.__get_pair_position()
        if pairx == NR_COLUMN - 1 or self.__cursorx == NR_COLUMN - 1:
            return
        if self.field[pairy][pairx + 1] != None and pairx + 1 != self.__cursorx:
            return
        if self.field[self.__cursory][self.__cursorx + 1] and self.__cursorx + 1 != pairx:
            return
        cur, pair = self.field[self.__cursory][self.__cursorx], self.field[pairy][pairx]
        self.field[pairy][pairx] = None
        self.field[self.__cursory][self.__cursorx] = None
        self.field[pairy][pairx + 1] = pair
        self.field[self.__cursory][self.__cursorx + 1] = cur
        self.__cursorx += 1

    def rotate (self):
        pairx, pairy = self.__get_pair_position()
        if self.__direction == DIRECTION_UP:
            # UP -> RIGHT
            newx = self.__cursorx + 1
            newy = self.__cursory
            newd = DIRECTION_RIGHT
        elif self.__direction == DIRECTION_RIGHT:
            # RIGHT -> DOWN
            newx = self.__cursorx
            newy = self.__cursory + 1
            newd = DIRECTION_DOWN
        elif self.__direction == DIRECTION_DOWN:
            # DOWN -> LEFT
            newx = self.__cursorx - 1
            newy = self.__cursory
            newd = DIRECTION_LEFT
        else:
            # LEFT -> UP
            newx = self.__cursorx
            newy = self.__cursory - 1
            newd = DIRECTION_UP
        if newx < 0 or newx >= NR_COLUMN or self.field[newy][newx] != None:
            return
        self.field[newy][newx] = self.field[pairy][pairx]
        self.field[pairy][pairx] = None
        self.__direction = newd

    def fall_periodic (self, column_ids = range(NR_COLUMN)):
        self.__fall_counter += 1
        if self.__fall_counter != self.__fall_period:
            return
        self.__fall_counter = 0
        self.fall(column_ids)

    def fall (self, column_ids = range(NR_COLUMN)):
        for column_id in column_ids:
            for row_id in range(NR_ROW - 1, 0, -1):
                if self.field[row_id][column_id] == None and self.field[row_id - 1][column_id] != None:
                    self.field[row_id][column_id] = self.field[row_id - 1][column_id]
                    self.field[row_id - 1][column_id] = None
        if self.__cursory != None:
            self.__cursory += 1

    def check_landing (self):
        for y in range(self.__cursory, NR_ROW):
            if self.field[y][self.__cursorx] == None:
                if self.__direction == DIRECTION_RIGHT or self.__direction == DIRECTION_LEFT:
                    pairx, pairy = self.__get_pair_position()
                    for y in range(pairy, NR_ROW):
                        if self.field[y][pairx] == None:
                            return False
                    return True
                return False
        return True

    def check_landing_all (self):
        for y in range(self.__cursory, NR_ROW):
            if self.field[y][self.__cursorx] == None:
                return False
        pairx, pairy = self.__get_pair_position()
        for y in range(pairy, NR_ROW):
            if self.field[y][pairx] == None:
                return False
        return True

    def reset_counter (self):
        self.__fall_counter = 0

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
freefall = False

def do_tick ():
    global freefall
    if freefall == False:
        field.fall_periodic()
        if field.check_landing():
            freefall = True
    else:
        field.fall()
        if field.check_landing_all():
            freefall = False
            field.newstone()
            field.reset_counter()
    field.draw()

def do_keyevent (event):
    if event.charCode == CHARCODE_UP:
        field.newstone()
    if freefall:
        return
    if event.charCode == CHARCODE_DOWN:
        pass
    elif event.charCode == CHARCODE_RIGHT:
        field.move_right()
    elif event.charCode == CHARCODE_LEFT:
        field.move_left()
    elif event.charCode == CHARCODE_SPACE:
        field.rotate()

document.bind("keypress", do_keyevent)
tick = timer.set_interval(do_tick, TIMER_TICK)
