print("Starting")

import board

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation

keyboard = KMKKeyboard()

keyboard.col_pins = (board.GP3, board.GP4, board.GP5,)
keyboard.row_pins = (board.GP7, board.GP6, board.GP2,)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

keyboard.keymap = [
    [KC.1, KC.2, KC.3,
     KC.4, KC.5, KC.6,
     KC.7, KC.8, KC.9
    ],
]

if __name__ == '__main__':
    keyboard.go()