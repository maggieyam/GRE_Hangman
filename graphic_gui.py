import tkinter
from tkinter import *
from PIL import ImageTk, Image
import string
import random
import graphics
import hangman

COMMON = "/Users/maggieyan/Desktop/cs106AP/GREHangman/common.csv"
BASIC = "/Users/maggieyan/Desktop/cs106AP/GREHangman/basic.csv"
ADVANCED = "/Users/maggieyan/Desktop/cs106AP/GREHangman/advanced.csv"

TITLE = "Hangman"
PATH = "/Users/maggieyan/Desktop/cs106AP/GREHangman/images/"
INITIAL_LIVES = 5
INITIAL_GUESSES = 8  # Initial number of guesses player starts with

# Window sizes for game categories
WINDOW1_WIDTH = 600  # Width of drawing window in pixels
WINDOW_HEIGHT1 = 500  # Height of drawing window for game categories in pixels
WINDOW1_X = 400  # Width of geometry format for window in pixels
WINDOW1_Y = 218  # Height of geometry format for window in pixels

# Window sizes for main game window
WINDOW2_WIDTH = 800  # Width of drawing window in pixels
WINDOW_HEIGHT2 = 600  # Height of drawing window in pixels
WINDOW2_X = 400  # Width of geometry format for window in pixels
WINDOW2_Y = 148  # Height of geometry format for window in pixels

# Window sizes for definition window
WINDOW3_WIDTH = 200  # Width of drawing window in pixels
WINDOW_HEIGHT3 = 10  # Height of drawing window in pixels
WINDOW3_X = 900  # Width of geometry format for window in pixels
WINDOW3_Y = 90  # Height of geometry format for window in pixels

CANVAS_WIDTH = 325  # Width of drawing canvas in pixels
CANVAS_HEIGHT = 520  # Height of drawing canvas in pixels
CANVAS_X = 160  # x-coordinate of canvas in pixels
CANVAS_Y = 80  # y-coordinate of canvas in pixels

NAME_WIDTH = 300   # Width of game name in pixels
NAME_HEIGHT = 100  # Height of game name in pixels
HEALTH_WIDTH = 250
HEALTH_HEIGHT = 40

BUTTON1_WIDTH = 150  # Width of word list choice buttons in pixels
BUTTON1_HEIGHT = 50  # Height of word list choice buttons in pixels
BUTTON2_WIDTH = 50  # Width of letter buttons in pixels
BUTTON2_HEIGHT = 50  # Height of letter buttons in pixels
BUTTON2_COORD = [(50, 150), (550, 90)]
BUTTON3_WIDTH = 100  # Width of function buttons in pixels
BUTTON3_HEIGHT = 30  # Height of function buttons in pixels
BUTTON3_COORD = [(20, 20), (20, 70), (610, 20)]

# Constant for the text settings
BG = 'grey20'
FONT_15 = 'Courier 15 bold'
FONT_17 = 'Courier 17 bold'
FONT_23 = 'Courier 23 bold'
FONT_27 = 'Courier 27 bold'
THICKNESS = 30

BUTTON1_IMAGE = ['sky_blue_button', 'yellow_button', 'red_button']
BUTTON1_TEXT = [(COMMON, 'Common'), (BASIC, 'Basic'), (ADVANCED, 'Advanced')]
BUTTON1_COLOR = ['cyan', 'brown1', 'gold']
BUTTON2_IMAGE = ["lilac", "lavender", "lime", "yellow", "green",
                 "sand", "blue", "cherry", "cyan"]
BUTTON3_IMAGE = ['cyan_button', 'red_button', 'yellow_button']
BUTTON3_TEXT = ['Next', 'Quit', 'Tips']
BUTTON3_COLOR = ['ghost white', 'ghost white', 'brown1']


def make_choice_gui():
    top = make_window(WINDOW1_WIDTH, WINDOW_HEIGHT1, WINDOW1_X, WINDOW1_Y, TITLE)
    make_button(top, "game_name", (150, 30), (NAME_WIDTH, NAME_HEIGHT))

    for i in range(3):
        coord = (230, 180 + (i * 70))
        size = (BUTTON1_WIDTH, BUTTON1_HEIGHT)
        text = BUTTON1_TEXT[i]

        btn = make_button(top, BUTTON1_IMAGE[i], coord, size)
        btn.config(text=text[1], fg=BUTTON1_COLOR[i], font=FONT_23)
        btn.config(command=lambda temp=text[0]: [top.destroy(), hangman.start_game(temp)])

    top.mainloop()


def make_gui(word, info):
    """
    This function sets up the canvas.
    @param  word
    @param  info        A dictionary contains original
                        word list and player information.
    returns the canvas
    """
    top = make_window(WINDOW2_WIDTH, WINDOW_HEIGHT2, WINDOW2_X, WINDOW2_Y, 'Hangman')
    canvas = make_canvas(top, info)
    make_entry(top, canvas, info)
    make_labels(top, info)
    make_letter_buttons(top, canvas, info)
    make_function_buttons(top, canvas, word, info)

    top.update()
    top.mainloop()


def make_labels(top, info):
    """
     @param  top    the main  window of the game
     @param  info   A dictionary contains original
                        word list and player information.
    """
    size = HEALTH_WIDTH, HEALTH_HEIGHT
    image = open_image(INITIAL_LIVES, HEALTH_WIDTH, HEALTH_HEIGHT)
    health = Label(top, anchor='nw', image=image, bd=0, background=BG)
    health.place(x=200, y=13, width=size[0], height=size[1])
    health.image = image
    info['health'] = health

    text = 'score:  ' + str(info.get('score'))
    score = Label(top, text=text, font=FONT_17)
    score.config(bg=BG, fg='yellow', anchor='e')
    score.place(x=360, y=95, width=105, height=30)
    info['label_score'] = score


def make_canvas(top, info):
    """
     @param  top    the main  window of the game
     @param  info   A dictionary contains original
                        word list and player information.
     returns the canvas                   
    """
    width = CANVAS_WIDTH
    height = CANVAS_HEIGHT
    canvas = Canvas(top, width=width, height=height, bg=BG)
    canvas.place(x=CANVAS_X, y=CANVAS_Y, width=width, height=height)
    graphics.draw_lines(canvas)
    graphics.make_text(canvas, info)

    return canvas


def make_entry(top, canvas, info):
    """
     @param  top     the main  window of the game
     @param  canvas  the canvas
     @param  info    A dictionary contains original
                        word list and player information.
    """
    entry = tkinter.Entry(top, width=8, name='entry')
    entry.place(x=360, y=140, width=105, height=25)
    entry.focus()
    entry.bind("<Return>", lambda event, e=entry:
               hangman.play_game(canvas, info, ""))
    info['entry'] = entry


def make_function_buttons(top, canvas, word, info):
    """
    @param  top         the main window of the game
    @param  canvas      Canvas
    @param  word
    @param  info        A dictionary contains original
                        word list and player information.
    """
    coord = BUTTON3_COORD
    size = (BUTTON3_WIDTH, BUTTON3_HEIGHT)
    for i in range(3):
        btn = make_button(top, BUTTON3_IMAGE[i], coord[i], size)
        btn.config(text=BUTTON3_TEXT[i], font=FONT_17, fg=BUTTON3_COLOR[i])
        if i == 0:  # Binds the 'Next' button
            info['next'] = btn
            btn.bind("<ButtonPress>", lambda event:
                     hangman.reset(canvas, word, info))
        elif i == 1:    # Binds the 'Quit' button
            btn.bind("<ButtonPress>", lambda event: top.destroy())
        elif i == 2:    # Binds the 'Tips' button
            btn.bind("<ButtonPress>", lambda event: make_definition(info))


def make_letter_buttons(top, canvas, info):
    """
    This function makes 26 letter buttons from A to Z and
    returns a list contains all letter buttons.

    @param  top         The main window of the game
    @param  canvas      Canvas
    @param  info        A dictionary contains original
                        word list and player information.
    """
    buttons = {}
    count_v = 0  # Counts vowels
    count_c = 0  # Counts consonants

    for char in string.ascii_uppercase:
        vowel = "A, E, I, O, U"
        if char in vowel:
            coord = BUTTON2_COORD[0]
            x = coord[0]
            y = coord[1] + count_v * 80
            count_v += 1
        else:
            coord = BUTTON2_COORD[1]
            x = coord[0] + (count_c // 7) * 80
            y = coord[1] + (count_c % 7 * 70)
            count_c += 1

        num = random.randrange(0, 9)
        size = (BUTTON2_WIDTH, BUTTON2_HEIGHT)
        btn = make_button(top, BUTTON2_IMAGE[num], (x, y), size)
        btn.bind("<ButtonPress>", lambda event, text=char:
                 hangman.play_game(canvas, info, text))
        btn.config(text=char, font=FONT_27)
        info[char] = btn
    return buttons


def make_definition(info):
    """
    @param  info    A dictionary contains original
                        word list and player information.
    """
    top = make_window(WINDOW3_WIDTH, WINDOW_HEIGHT3, WINDOW3_X, WINDOW3_Y, 'Definition')

    temp = info.get('tips')
    text = temp.split()

    tips = Label(top, text=text, font=FONT_17)
    tips.config(bg=BG, fg='white', wraplength=400, justify='center')
    tips.grid(row=0, column=0, padx=50, pady=50)
    tips.focus()
    tips.bind("<FocusOut>", lambda event: [Tk.destroy(top), top.quit()])

    top.mainloop()


def make_window(width, height, x, y, title):
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    top.configure(background=BG)
    top.geometry("+{}+{}".format(x, y))

    return top


def make_button(top, file, coord, size):

    image = open_image(file, size[0], size[1])
    btn = Button(top, image=image, highlightbackground=BG)
    btn.place(x=coord[0], y=coord[1], width=size[0], height=size[1])
    btn.config(compound=CENTER, highlightthickness=THICKNESS)
    btn.image = image

    return btn


def update_entry(entry):
    """
    This function deletes the previous letter has
    been entered

    @param entry       the entry to enter the letter
    """
    entry.delete(0, END)
    entry.insert(0, " ")


def reset_widgets(canvas, info):
    """
    @param  canvas      Canvas
    @param  info        A dictionary contains original
                        word list and player information.
    """
    # Updates score label
    info.get('label_score').config(text=info.get('score'))

    # Updates entry
    entry = info.get('entry')
    update_entry(entry)
    entry.bind("<Return>", lambda event, e=entry:
               hangman.play_game(canvas, info, ""))

    # Enable used buttons
    for letter in info.get('used'):
        btn = info.get(letter)
        btn.config(state='normal')
        btn.bind("<ButtonPress>", lambda event, text=letter:
                 hangman.play_game(canvas, info, text))

    # Updates health bar image
    image = open_image(info.get('lives'), HEALTH_WIDTH, HEALTH_HEIGHT)
    health = info.get('health')
    health.config(image=image)
    health.image = image


def open_image(file, width, height):
    """
    @param  file    image file name
    @param  width   width of the resized image
    @param  height  height of the resized image
    returns the resized image
    """
    image = Image.open(PATH + str(file) + '.png')
    image = image.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)


