##############################################################################
#
# nisepuyo-brython
#   Copyright (C) 2021 kWatanabe
#   Released under the GNU General Public License version 2.
#   See "LISENSE" file
#            or https://github.com/wwatchin/nisepuyo-brython/blob/main/LICENSE
#
##############################################################################

from browser import document
from browser import html
from browser import timer
import random

# debug
debug = document["debugarea"]
def msg (s):
    debug.text = str(s)

# Keycode
CHARCODE_UP = 119
CHARCODE_LEFT = 97
CHARCODE_DOWN = 115
CHARCODE_RIGHT = 100
CHARCODE_SPACE = 32

# Size and number
STONE_SIZE = 32
NR_ROW = 12
NR_COLUMN = 6
FIELD_WIDTH = NR_COLUMN * STONE_SIZE
FIELD_HEIGHT = NR_ROW * STONE_SIZE

# Position
POSX_NEWSTONE = 2
POSY_NEWSTONE = 1
DIRECTION_UP, DIRECTION_RIGHT, DIRECTION_DOWN, DIRECTION_LEFT = range(4)
POS_PAIRSTONE = ((0, -1), (1, 0), (0, 1), (-1, 0))

# Parameter
TIMER_TICK = 25

# Stones
images_stone = (html.IMG(src="img/stone0.png"), html.IMG(src="img/stone1.png"),
                html.IMG(src="img/stone2.png"), html.IMG(src="img/stone3.png"),
                html.IMG(src="img/stone4.png"), html.IMG(src="img/stone5.png"))
UNERASABLE_STONE = 0
NR_ERASE_STONES = 4

###
### Classes.
###
# Field
class Field ():
    def __init__ (self, context, images_stone, posx = 0, posy = 0, period = 20):
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
        self.set_force_fall_mode(False)
        self.reset_counter()
        self.clear()

    def __get_pair_position (self):
        """
        Get position of the pair stone.
        """
        return (self.__cursorx + POS_PAIRSTONE[self.__direction][0],
                self.__cursory + POS_PAIRSTONE[self.__direction][1])

    def draw (self):
        """
        Draw a field on canvas.
        """
        self.__context.clearRect(self.__x, self.__y, self.__endx, self.__endy)
        y = self.__y
        for row in self.field:
            x = self.__x
            for cell in row:
                if cell != None:
                    self.__context.drawImage(self.__images_stone[cell], x, y)
                x += STONE_SIZE
            y += STONE_SIZE
        return

    def newstone (self):
        """
        Add new a pair of stones.
        """
        self.__cursorx = POSX_NEWSTONE
        self.__cursory = POSY_NEWSTONE
        self.__direction = DIRECTION_UP
        self.field[POSY_NEWSTONE-1][POSX_NEWSTONE] = random.randint(1, self.__nr_stones)
        self.field[POSY_NEWSTONE][POSX_NEWSTONE] = random.randint(1, self.__nr_stones)
        return

    def move_left (self):
        """
        Move stones to left.
        """
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
        return

    def move_right (self):
        """
        Move stones to right.
        """
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
        return

    def rotate (self):
        """
        Rotate stones.
        """
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
        return

    def fall_periodic (self, column_ids = range(NR_COLUMN)):
        """
        Fall all stones periodically.
        """
        if self.__fall_forced == False:
            self.__fall_counter += 1
            if self.__fall_counter < self.__fall_period:
                return
        else:
            self.__fall_forced = False
        self.fall(column_ids)
        self.__fall_counter = 0
        return

    def fall (self, column_ids = range(NR_COLUMN)):
        """
        Fall all stones.
        """
        for column_id in column_ids:
            for row_id in range(NR_ROW - 1, 0, -1):
                if self.field[row_id][column_id] == None and self.field[row_id - 1][column_id] != None:
                    self.field[row_id][column_id] = self.field[row_id - 1][column_id]
                    self.field[row_id - 1][column_id] = None
        if self.__cursory != None:
            self.__cursory += 1

    def check_landing (self):
        """
        Make sure a stone has landed.
        """
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

    def check_landing_all_lazy (self):
        """
        Make sure all stones have landed. (lazy)
        """
        for y in range(self.__cursory, NR_ROW):
            if self.field[y][self.__cursorx] == None:
                return False
        pairx, pairy = self.__get_pair_position()
        for y in range(pairy, NR_ROW):
            if self.field[y][pairx] == None:
                return False
        return True

    def check_landing_all_strict (self):
        """
        Make sure all stones have landed. (strict)
        """
        for x in range(NR_COLUMN):
            found = (self.field[NR_ROW - 1][x] != None)
            for y in range(NR_ROW - 2, -1, -1):
                if found == False and self.field[y][x] != None:
                    return False
                elif found == True and self.field[y][x] == None:
                    found = False
        return True
        
    def __erase_stones_sub (self, x, y, stone):
        """
        check and erase stones (sub routine)
        """
        if self.field[y][x] != stone:
            return
        if (x, y) in self.__candidate:
            return
        self.__candidate.append((x, y))
        if y > 0: self.__erase_stones_sub(x, y - 1, stone)
        if y < NR_ROW - 1: self.__erase_stones_sub(x, y + 1, stone)
        if x > 0: self.__erase_stones_sub(x - 1, y, stone)
        if x < NR_COLUMN - 1: self.__erase_stones_sub(x + 1, y, stone)
        return

    def erase_stones (self):
        """
        check and erase stones
        """
        erased = False
        for y in range(NR_ROW):
            for x in range(NR_COLUMN):
                if self.field[y][x] == None:
                    continue
                self.__candidate = []
                self.__erase_stones_sub(x, y, self.field[y][x])
                if len(self.__candidate) >= NR_ERASE_STONES:
                    for x, y in self.__candidate:
                        self.field[y][x] = None
                    erased = True
        return erased
        
    def set_force_fall_mode (self, forced = True):
        """
        Set the fall mode to "Forced" or "None"
        """
        self.__fall_forced = forced

    def reset_counter (self):
        """
        Set the fall counter to Zero.
        """
        self.__fall_counter = 0

    def gameover (self):
        """
        Direct the game over.
        """
        self.field = [[UNERASABLE_STONE if stone != None else None for stone in row] for row in self.field]
        self.draw()

    def check_gameover (self):
        """
        Check if there is a stone in the spout.
        """
        return (self.field[POSY_NEWSTONE][POSX_NEWSTONE] != None)

    def clear (self):
        """
        Delete all stones on field.
        """
        self.field = [[None] * NR_COLUMN for i in range(NR_ROW)]

###
### Main routine.
###
canvas = document["drawarea"]
context = canvas.getContext("2d")
field = Field(context, images_stone)
freefall = False
erased = False
gameover = False

def newstone():
    global freefall
    global gameover
    gameover = field.check_gameover()
    if gameover == True:
        field.gameover()
        return
    freefall = False
    field.newstone()
    field.reset_counter()

def do_tick ():
    global freefall
    global erased
    if gameover:
        return
    if freefall == False:
        field.fall_periodic()
        if field.check_landing():
            freefall = True
    else:
        field.fall()
        if erased == False:
            if field.check_landing_all_lazy():
                erased = field.erase_stones()
                if erased == False:
                    newstone()
        else:
            if field.check_landing_all_strict():
                erased = field.erase_stones()
                if erased == False:
                    newstone()
    field.draw()

def do_keyevent (event):
    if gameover:
        return
    if event.charCode == CHARCODE_UP:
        field.newstone()
    if freefall:
        return
    if event.charCode == CHARCODE_DOWN:
        field.set_force_fall_mode(True)
    elif event.charCode == CHARCODE_RIGHT:
        field.move_right()
    elif event.charCode == CHARCODE_LEFT:
        field.move_left()
    elif event.charCode == CHARCODE_SPACE:
        field.rotate()

document.bind("keypress", do_keyevent)
tick = timer.set_interval(do_tick, TIMER_TICK)
