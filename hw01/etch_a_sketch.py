#!/usr/bin/env python3
import curses
import time

BEGIN_X = 20
BEGIN_Y = 7
ACTUAL_HEIGHT = 20
ACTUAL_WIDTH = 15

def model_pos_to_view_pos(y, x):
    """
        Map model postion to view position
    """
    return y + 1, 3 + 2 * x

HEIGHT, WIDTH = model_pos_to_view_pos(ACTUAL_HEIGHT, ACTUAL_WIDTH)

def addstr(win, y, x, string):
    """
        Wrapper for view to add string 
    """
    view_y, view_x = model_pos_to_view_pos(y, x)
    win.addstr(view_y, view_x, string)

def draw(win, status, curse_position):
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
    addstr(win, curse_position[0], curse_position[1], '')
    win.refresh()

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

def clear_status():
    """
        Clear window
    """
    return [
        [0 for i in range(WIDTH)]
        for i in range(HEIGHT)
    ]

def main(stdscr):
    stdscr.clear()

    win = curses.newwin(HEIGHT, WIDTH, BEGIN_Y, BEGIN_X)
    win.keypad(True)
    status = clear_status()
    curse_position = [0, 0]
    win.addstr(0, 0, 'Etch-a-Sketch\n Movements: Keys UP & DOWN,\n                 LEFT &  RIGHT\n Key SPACE - draw\n c - clear\n r - erase\n q - exit ')
    while(1):   
        input_key = win.getkey()
        if input_key in ['KEY_DOWN', 'KEY_UP', 'KEY_LEFT', 'KEY_RIGHT']:
            curse_position = move_curse(curse_position, input_key)
        if input_key == ' ':
            status[curse_position[0]][curse_position[1]] = 1
        if input_key == 'c':
            status = clear_status()
        if input_key == 'r':
            status[curse_position[0]][curse_position[1]] = 0
        if input_key == 'q':
            break
        draw(win, status, curse_position)

curses.wrapper(main)
