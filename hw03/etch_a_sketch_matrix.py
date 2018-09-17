#!/usr/bin/env python3
import smbus
import time
from Adafruit_BBIO.Encoder import RotaryEncoder, eQEP1, eQEP2
import Adafruit_BBIO.GPIO as GPIO
import curses
import argparse

#Initialize matrix
bus = smbus.SMBus(2) #Use i2c bus 1
matrix = 0x70        #Use address 0x70 for matrix

delay = 1            #Delay between images in second
bus.write_byte_data(matrix, 0x21, 0) #Start oscillator
bus.write_byte_data(matrix, 0x81, 0) #Disp on, blink off
bus.write_byte_data(matrix, 0xe7, 0) #Full brightness

#Initialize encoder
myEncoder_1 = RotaryEncoder(eQEP1)
myEncoder_1.setAbsolute()
myEncoder_1.enable()
myEncoder_2 = RotaryEncoder(eQEP2)
myEncoder_2.setAbsolute()
myEncoder_2.enable()
def model_pos_to_view_pos(y, x):
    """
        Map model position to view position
    """
    return y + 1, 3 + 2 * x

def clear_status(height, width):
    """
        Clear window
    """
    return [
        [0 for i in range(width)]
        for i in range(height)
    ]

def clear_matrix_status():
    """
        Clear matrix
    """
    return [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
parser = argparse.ArgumentParser()
parser.add_argument('HEIGHT', type=int, help='HEIGHT of the game')
parser.add_argument('WIDTH', type=int, help='WIDTH of the game')
args = parser.parse_args()

ACTUAL_HEIGHT =  args.HEIGHT
ACTUAL_WIDTH = args.WIDTH
HEIGHT, WIDTH = model_pos_to_view_pos(ACTUAL_HEIGHT, ACTUAL_WIDTH)
status = clear_status(HEIGHT, WIDTH)
curse_position = [0, 0]
current_rotary_position_1 = myEncoder_1.position
current_rotary_position_2 = myEncoder_2.position

def addstr(win, y, x, string):
    """
        Wrapper for view to add string 
    """
    view_y, view_x = model_pos_to_view_pos(y, x)
    win.addstr(view_y, view_x, string)

def draw_to_window(win, status, curse_position):
    """
        Draw the current screen from the model
        win: window object, from curses
        status: 2d array, the status of the canvas
            0: the slot is not drawn
            1: the slot has been drawn
        curse_position: [y, x], the position of the curse
    """
    win.clear()
    # draw border
    for x in range(ACTUAL_WIDTH):
        if x < 10:
            win.addstr(0, 3 + 2 * x, '{}'.format(x))
        else:
            win.addstr(0, 2 + 2 * x, '{}'.format(x))
    for y in range(HEIGHT - 1):
        if y < 10:
            win.addstr(y + 1, 1, '{}:'.format(y))
        else:
            win.addstr(y + 1, 0, '{}:'.format(y))
    # draw status and curse
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if status[y][x] != 0:
                addstr(win, y, x, 'x')
    addstr(win, curse_position[0], curse_position[1], '+')
    win.refresh()

def inverse_x(x):
    global ACTUAL_WIDTH
    return ACTUAL_WIDTH - 1 - x

def inverse_y(y):
    global ACTUAL_HEIGHT
    return ACTUAL_HEIGHT - 1 - y

def draw_to_matrix():
    global status
    global curse_position
    global bus
    global matrix
    matrix_array = clear_matrix_status()
    #draw status
    for x in range(ACTUAL_WIDTH):
        green = 0
        red = 0
        for y in range(ACTUAL_HEIGHT):
            if status[y][inverse_x(x)] == 1:
                green += 1 << y
        matrix_array[2 * x] = green
        matrix_array[2 * x + 1] = red
    #draw current curse position
    matrix_array[2 * inverse_x(curse_position[1]) + 1] += 1 << curse_position[0] 
    bus.write_i2c_block_data(matrix, 0, matrix_array)

def move_curse(curse_position, key):
    """
        Move the curse, and check if the new location is valid
        key: string, in ('KEY_DOWN', 'KEY_UP', 'KEY_LEFT', 'KEY_RIGHT')
    """
    if key == 'KEY_DOWN':
        if curse_position[0] < ACTUAL_HEIGHT - 1:
            return [curse_position[0] + 1, curse_position[1]]
    if key == 'KEY_UP':
        if curse_position[0] > 0:
            return [curse_position[0] - 1, curse_position[1]]
    if key == 'KEY_LEFT':
        if curse_position[1] > 0:
            return [curse_position[0], curse_position[1] - 1]
    if key == 'KEY_RIGHT':
        if curse_position[1] < ACTUAL_WIDTH - 1:
            return [curse_position[0], curse_position[1] + 1]
    return curse_position

BEGIN_X = 0
BEGIN_Y = 0

button_1 = "P9_15"
button_2 = "P9_17"
button_3 = "P9_16"
button_4 = "P9_18"
button_5 = "P9_21"
button_6 = "P9_22"
button_7 = "P9_24"

GPIO.setup(button_1, GPIO.IN)
GPIO.setup(button_2, GPIO.IN)
GPIO.setup(button_3, GPIO.IN)
GPIO.setup(button_4, GPIO.IN)
GPIO.setup(button_5, GPIO.IN)
GPIO.setup(button_6, GPIO.IN)
GPIO.setup(button_7, GPIO.IN)

map = { button_1: 'KEY_UP',
        button_2: 'KEY_DOWN',
        button_3: 'KEY_LEFT',
        button_4: 'KEY_RIGHT',
        button_5: ' ',
        button_6: 'c',
        button_7: 'r'
        }

def updateCanvas(channel):
    global status
    global curse_position
    state = GPIO.input(channel)
    if state == 1:
        input_key = map[channel]
        if input_key in ['KEY_DOWN', 'KEY_UP', 'KEY_LEFT', 'KEY_RIGHT']:
            curse_position = move_curse(curse_position, input_key)
        if input_key == ' ':
            status[curse_position[0]][curse_position[1]] = 1
        if input_key == 'c': 
            status = clear_status(len(status), len(status[0])) 
        if input_key == 'r': 
            status[curse_position[0]][curse_position[1]] = 0 


GPIO.add_event_detect(button_1, GPIO.BOTH, callback=updateCanvas)
GPIO.add_event_detect(button_2, GPIO.BOTH, callback=updateCanvas)
GPIO.add_event_detect(button_3, GPIO.BOTH, callback=updateCanvas)
GPIO.add_event_detect(button_4, GPIO.BOTH, callback=updateCanvas)
GPIO.add_event_detect(button_5, GPIO.BOTH, callback=updateCanvas)
GPIO.add_event_detect(button_6, GPIO.BOTH, callback=updateCanvas)
GPIO.add_event_detect(button_7, GPIO.BOTH, callback=updateCanvas)

def track_rotary():
    global myEncoder
    global curse_position
    global current_rotary_position_1
    global current_rotary_position_2
    new_rotary_position_1 = myEncoder_1.position
    new_rotary_position_2 = myEncoder_2.position
    if new_rotary_position_1 > current_rotary_position_1:
        if curse_position[0] > 0:
            curse_position[0] -= 1
    if new_rotary_position_1 < current_rotary_position_1:
        if curse_position[0] < ACTUAL_HEIGHT - 1:
            curse_position[0] += 1
    if new_rotary_position_2 > current_rotary_position_2:
        if curse_position[1] > 0:
            curse_position[1] -= 1
    if new_rotary_position_2 < current_rotary_position_2:
        if curse_position[1] < ACTUAL_WIDTH - 1:
            curse_position[1] += 1
    current_rotary_position_1 = new_rotary_position_1
    current_rotary_position_2 = new_rotary_position_2

def main(stdscr):
    stdscr.clear()
    
    win = curses.newwin(HEIGHT, WIDTH, BEGIN_Y, BEGIN_X)
    win.keypad(True)
    win.addstr(0, 0, 'Etch-a-Sketch\n Movements: Keys UP & DOWN,\n                 LEFT &  RIGHT\n Key SPACE - draw\n c - clear\n r - erase\n q - exit ')
    while(1):   
       draw_to_window(win, status, curse_position)
       draw_to_matrix()
       track_rotary()
       time.sleep(1.0 / 10)

curses.wrapper(main)

