"""
File: word_guess.py
-------------------
This program emulates the word game "Hangman". The program
randomly chooses a word from the dictionary, and asks the
player to guess corresponding letters.

For each incorrect letter, the program draws a part of the
"man." The game ends when the canvas finishes drawing the
man. For each correct letter, the player collects 10 points,
exponentially increasing with each consecutively correct
letter. For each correct word, the player collects at 50
points, exponentially increasing with consecutively correct
words. The total point is cumulative until the player quits.
"""
import graphics
import graphic_gui
import dictionary

INITIAL_GUESSES = 8  # Initial number of guesses player starts with
INITIAL_LIVES = 5


def main():
    """
    To play the game, we first select the secret word for the
    player to guess. If the player guessed a wrong letter, the
    canvas will start drawing a hangman. In each round, the player
    can guess no more than 8 wrong letters.

    """
    graphic_gui.make_choice_gui()


def start_game(file):
    """
    This function
    @param  file
    """
    word = dictionary.get_dict(file)
    info = {'guess': INITIAL_GUESSES, 'lives': INITIAL_LIVES,
            'score': 0, 'correct': 0, 'skip': 1}
    info = dictionary.get_word(word, info)
    graphic_gui.make_gui(word, info)


def reset(canvas, word, info):
    """
    This function resets the game
    @param  canvas      Canvas
    @param  word
    @param  info        A dictionary contains original
                        word list and player information.
    """

    info['lives'] -= 1
    graphic_gui.reset_widgets(canvas, info)
    if info.get('lives') == 0:
        graphics.end_scene(canvas, info)
    else:
        graphics.draw_lines(canvas)
        word = dictionary.get_word(word, info)
        graphics.make_text(canvas, word)

    # info['skip'] = 1
    info['guess'] = INITIAL_GUESSES
    info['correct'] = 0


def play_game(canvas, info, letter):
    """
    This function gets the letter that the player entered in the entry,
    and transfer it to upper case. If the letter is unused and in the
    original secret word, the player's receive points; Otherwise, will
    draw hangman on the canvas.

    @param  canvas      Canvas
    @param  entry       Entry widget to type inputs
    @param  buttons     A list contains button widgets
    @param  info        A dictionary contains original
                        word list and player information.
    @param  letter
    """
    if is_valid_game(info, letter):
        inputs = get_input(letter, info.get('entry'))
        if len(inputs) > 1:
            win = check_word(info, inputs)
        elif len(inputs) == 1:
            win = check_letter(canvas, info, inputs)

        if win:
            graphics.win(canvas, info)
        else:
            graphics.draw_hangman(canvas, info)


def is_valid_game(info, letter):
    """
    This function returns if the there is no guesses left and if the
    player's answer is the same as the secret word.

    @param  info        A dictionary contains original
                        word list and player information.
    @param  letter
    """
    if info.get('input') == info.get('answer') or info.get('guess') == 0:
        return False

    entry = info.get('entry')
    inputs = edited_input(entry)
    if letter == "" and not inputs.isalpha():
        graphic_gui.update_entry(entry)
        return False
    return True


def edited_input(entry):
    inputs = entry.get()
    inputs = inputs.strip()
    return inputs.upper()


def get_input(letter, entry):
    """
    @param  entry       Entry widget to type inputs
    @param  letter
    returns
    """
    if letter == "":
        inputs = edited_input(entry)
        graphic_gui.update_entry(entry)
    else:
        inputs = letter
    return inputs


def check_word(info, inputs):
    """
    @param  canvas      Canvas
    @param  info        A dictionary contains original
                        word list and player information.
    @param  inputs
    """
    if inputs == info.get('answer'):
        info['skip'] = 0
        return True
    info['guess'] -= 1
    return False


def check_letter(canvas, info, inputs):
    """
    @param  canvas      Canvas
    @param  buttons     A list contains button widgets
    @param  info        A dictionary contains original
                        word list and player information.
    @param  inputs
    """
    used = info.get('used')
    if used.find(inputs) < 0:  # Checks if the letter is used
        search_letter(info, inputs)
        # Updates the window
        if info.get('input') == info.get('answer'):
            info['skip'] = 0
            return True
        canvas.itemconfig('answer', text=info.get('input'))
        btn = info.get(inputs)
        btn.config(state='disabled')
    return False


def search_letter(info, letter):
    """
    This function finds the letter that is in the
    secret word and updates the word_list.
    @param  canvas      Canvas
    @param  info        A dictionary contains original
                        word list and player information.
    @param letter       The letter the player guessed
    """
    answer = info.get('answer')
    if answer.find(letter) >= 0:
        info['correct'] += 1
        edit_player_word(info, letter)
        correct = info.get('correct')
        info['score'] += 10 + correct ** 3
        score = info.get('score')
        info['label_score'].config(text=score)
    else:
        info['guess'] -= 1
        # clear the count of correct answers in row
        info['correct'] = 0
    info['used'] += letter


def edit_player_word(info, letter):
    """
    This function finds the letter that is in the
    secret word and updates the word for the player.

    @param  info        A dictionary contains original
                        word list and player information.
    @param letter:      The letter the player guessed
    """
    answer = info.get('answer')
    while answer.find(letter) >= 0:
        inputs = info.get('input')
        index = answer.find(letter)
        info['input'] = inputs[: index] + letter + inputs[index + 1:]
        answer = answer[: index] + '-' + answer[index + 1:]


if __name__ == "__main__":
    main()
