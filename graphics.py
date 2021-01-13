"""
File: graphic.py
-------------------
This program draws a canvas that allows the player to
play the word game. The player can either use the keyboard
to input guesses or click on the 26 letters to play. The program also draws
the hangman and shows text and scores.
"""

import time

INITIAL_LIVES = 5

CANVAS_WIDTH = 325  # Width of drawing canvas in pixels
CANVAS_HEIGHT = 500  # Height of drawing canvas in pixels
CENTER_X = CANVAS_WIDTH / 2  # Width of the center of canvas
CENTER_Y = CANVAS_HEIGHT / 2  # Height of the center of canvas

# Constants for the ground
START_X = 10  # x-coordinate point of the ground

END_X = CANVAS_WIDTH - START_X  # x-coordinate point of the ground (right)
END_Y = CANVAS_HEIGHT - 70  # y-coordinate point of the ground(right)

# Constant for the pole and the string
POLE_X = START_X + 60  # x-coordinate of the vertical pole
POLE_Y = 150  # y-coordinate point of the vertical-pole
STRING_X = POLE_X + 110  # x-coordinate of the string
STRING_Y = POLE_Y + 30  # y-coordinate of the lower end of the string

# Constant for the head
HEAD_SIZE = 60
HEAD_L = STRING_X - HEAD_SIZE / 2  # x-coordinate of the head (left-top)
HEAD_R = HEAD_L + HEAD_SIZE
NECK_Y = STRING_Y + HEAD_SIZE

# Constant for the text settings
FG = 'white'
FONT_20 = 'Helvetica 20 bold'
FONT_30 = 'Helvetica 30 bold'
FONT_50 = 'Courier 20 bold'


def make_text(canvas, info):
    """
    @param  canvas      Canvas
    @param  info        A dictionary contains original
                        word list and player information.
    """
    text = info.get('input')
    center_x = (CANVAS_WIDTH - len(text)) / 2
    start_y = CANVAS_HEIGHT - 30
    canvas.create_text(center_x, start_y, text=text, font=FONT_30, fill=FG, tags='answer')
    canvas.create_text(110, 73, text="Your answer: ", font=FONT_50, fill=FG)


def draw_lines(canvas):
    """
    This function draws the hangman in the canvas
    @param canvas      Canvas
    """
    # draws pole
    canvas.create_line(POLE_X, POLE_Y, POLE_X, END_Y, tags='t7')
    canvas.itemconfig('t7', fill=FG, width=3)
    # draws string
    canvas.create_line(POLE_X, POLE_Y, STRING_X, POLE_Y, tags='t6')
    canvas.create_line(STRING_X, POLE_Y, STRING_X, STRING_Y, tags=('t6', 'string'))
    canvas.itemconfig('t6', fill=FG, width=3)
    # draws head
    canvas.create_oval(HEAD_L, STRING_Y, HEAD_R, NECK_Y, tags=('t5', 'head', 'man'))
    canvas.itemconfig("head", outline=FG, width=2)
    # draws_torso()
    canvas.create_line(STRING_X, NECK_Y, STRING_X, NECK_Y + 80, tags=('t4', 'body', 'man'))
    # draws left_hand()
    canvas.create_line(STRING_X, NECK_Y + 38, STRING_X - 38, NECK_Y, tags=('t3', 'body', 'man'))
    # draws right_hand()
    canvas.create_line(STRING_X, NECK_Y + 38, STRING_X + 38, NECK_Y, tags=('t2', 'body', 'man'))
    # draws left_leg()
    canvas.create_line(STRING_X, NECK_Y + 80, STRING_X - 38, NECK_Y + 118, tags=('t1', 'body', 'man'))
    # draws right_leg()
    canvas.create_line(STRING_X, NECK_Y + 80, STRING_X + 38, NECK_Y + 118, tags=('t0', 'body', 'man'))

    canvas.itemconfig('body', fill=FG, width=2)
    canvas.itemconfig('all', state='hidden')
    # draws ground
    canvas.create_line(START_X, END_Y, END_X, END_Y, fill=FG, width=4)


def draw_hangman(canvas, info):
    """
    @param  canvas  Canvas
    @param  info     number of wrong guesses available
    """
    num = info.get('guess')
    canvas.itemconfig('t' + str(num), state='normal')
    if num == 0:
        lose(canvas, info)


def win(canvas, info):
    """
    This function updates the canvas when the round is finished.

    @param  canvas      Canvas
    @param  info        A dictionary contains original
                        word list and player information.
    """
    answer = info.get('answer')
    info['input'] = answer
    info['score'] += len(answer) ** 2 + 50
    score = info.get('score')
    info['label_score'].config(text=score)
    canvas.itemconfig('answer', text=info.get('input'))
    canvas.itemconfig('all', state='normal')
    pull_strings(canvas, 35, 2, 2)
    pull_strings(canvas, 11, -3, 0)
    man_move(canvas, 'man', 4, 0)
    info['lives'] += 1


def lose(canvas, info):
    """
    @param  canvas
    @param  info
    """
    canvas.itemconfig("body", fill="red")
    canvas.itemconfig("head", outline="red")
    canvas.itemconfig("answer", text=info.get('answer'), fill='red')
    if info.get('lives') == 1:
        end_scene(canvas, info)


def end_scene(canvas, info):
    info['lives'] = INITIAL_LIVES + 1
    info['score'] = 0
    canvas.itemconfig('all', state='hidden')
    canvas.create_text(150, 250, text='GAME OVER', fill='white', font='Courier 50 bold')


def pull_strings(canvas, dy, dir1, dir2):
    while dy > 0:
        for i in range(dy):
            canvas.coords("string", STRING_X, POLE_Y, STRING_X, STRING_Y + i * dir1)
            canvas.move("head", 0, dir2)
            canvas.move("body", 0, dir2)
            animation(canvas, 0.001)
            dy -= i

def man_move(canvas, object, dx, dy):
    while canvas.coords(object)[0] <= CANVAS_WIDTH and canvas.coords(object)[1] <= CANVAS_HEIGHT + 100:
        canvas.move(object, dx, dy)
        animation(canvas, 0.001)
        
def animation(canvas, delay):
    """
    This function creates animation effects.

    @param canvas   Canvas
    @param delay
    """
    canvas.update()
    time.sleep(delay)


def show_tips(canvas):
    """
    This function reminds the player enter more than
    one single letter or a letter has been used.

    @param canvas      the canvas
    """

    text = 'This letter has been used'
    tips = canvas.create_text(CENTER_X, 60, font=FONT_20, text=text, fill='yellow')
    animation(canvas, 0.8)
    canvas.itemconfig(tips, text='')








