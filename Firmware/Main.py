print("Starting")

# KMK Firmware Configuration File

# Import necessary modules from KMK and board library
import board

from kmk.modules.encoder import EncoderHanlder
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()

# Define the keyboard matrix configuration and encoder pins

# Define column and row pins for the keyboard matrix
keyboard.col_pins = (board.GP3, board.GP4, board.GP5,) # Columns pins 
keyboard.row_pins = (board.GP7, board.GP6, board.GP2,) # Rows pins
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Add media keys extension to the keyboard
keyboard.extensions.append(MediaKeys())

# initialize layers module
layers = Layers()
keyboard.modules.append(layers)

# initialize the encoder module
encoder_handler = EncoderHanlder()

# Define the pins for the rotary encoders
encoder_handler.pins = (
    (board.GP9, board.GP9, None), # Encoder 1 pins A and B
    (board.GP11, board.GP10, None), # Encoder 2 pins A and B
)

# Map encoder actions to keycodes
# layer format: Layer 0, Layer 1, Layer 2, ...
encoder_handler.map = [
    ( # Layer 0 (base layer)
        (KC.NO, KC.NO, KC.NO), # Encoder 1 actions (Layer switching)
        (KC.LCTL(KC.UP), KC.LCTL(KC.DOWN), KC.NO)  # Encoder 2 actions (Scrolling)
    )
    ( # Layer 1
        (KC.NO, KC.NO, KC.NO), # Encoder 1 actions (Layer switching)
        (KC.PLUS, KC.MINUS, KC.NO)  # Encoder 2 actions (zooming in cad)
    )
    ( # Layer 2
        (KC.NO, KC.NO, KC.NO), # Encoder 1 actions (Layer switching)
        (KC.VOLU, KC.VOLD, KC.NO)  # Encoder 2 actions (Volume control)
    )
    ( # Layer 3
        (KC.NO, KC.NO, KC.NO), # Encoder 1 actions (Layer switching)
        (KC.LCTL(KC.EQUAL), KC.LCTL(KC.MINUS), KC.NO)  # Encoder 2 actions (no action)
    )
]

# Override encoder handler to add layer switching logic
_original_on_move = encoder_handler.on_move_do

def layer_switching_encoder(key, keyboard, state):
    if state['encoder'] == 0:  # First encoder controls layers
        current_layer = keyboard.active_layers[0]
        total_layers = len(keyboard.keymap)
        
        if state['direction'] == 1:  # Clockwise
            next_layer = (current_layer + 1) % total_layers
            keyboard.active_layers[0] = next_layer
        else:  # Counter-clockwise
            next_layer = (current_layer - 1) % total_layers
            keyboard.active_layers[0] = next_layer
    else:
        # For other encoders, use normal behavior
        _original_on_move(key, keyboard, state)

encoder_handler.on_move_do = layer_switching_encoder

keyboard.modules.append(encoder_handler)

# Define the keymap for the keyboard
# The keymap is not done yet i dont know what i want on it
keyboard.keymap = [
    # Layer 0 (base layer) coding layer
    [
        KC.LCTL(KC.LSFT(KC.P)),    KC.LCTL(KC.S),    KC.F12,
        KC.LCTL(KC.C),    KC.LCTL(KC.V),    KC.LCTL(KC.SLSH),
        KC.LCTL(KC.Z),    KC.F5,    KC.LCTL(KC.F),
    ],
    # Layer 1 Fusion 360 layer
    [
        KC.HOME,   KC.S,   KC.LSFT(KC.F),
        KC.E,   KC.F,   KC.O,
        KC.R,   KC.Q,   KC.V,
    ],
    # Layer 2 Gaming layer
    [
    KC.LCTL(KC.LSFT(KC.ESC)),   KC.MUTE,   KC.MPLY,
        KC.F13,   KC.TAB,   KC.PSCR,
        KC.M,   KC.MPRV,   KC.MNXT,    
    ],
        # Layer 3 Advanced Coding layer
    [
        KC.LCTL(KC.T),   KC.LCTL(KC.LSFT(KC.F)),   KC.LCTL(KC.BSLS),
        KC.LCTL(KC.A),   KC.LCTL(KC.D),   KC.F2,
        KC.LCTL(KC.P),   KC.LCTL(KC.G),   KC.LCTL(KC.DOT),    
    ],
]

if __name__ == '__main__':
    keyboard.go()