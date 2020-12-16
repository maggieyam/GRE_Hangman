"""
File: infoary.py
-------------------
This program emulates the word game "Hangman". The program
randomly chooses a word from the infoary, and asks the
player to guess corresponding letters.

For each incorrect letter, the program draws a part of the
"man." The game ends when the canvas finishes drawing the
man. For each correct letter, the player collects 10 points,
exponentially increasing with each consecutively correct
letter. For each correct word, the player collects at 50
points, exponentially increasing with consecutively correct
words. The total point is cumulative until the player quits.
"""

import random


def get_dict(file):
    """
    This function returns a secret word that the player is trying
    to guess in the game.  This function selects a random word from
    one of the three lists: 'common.csv', 'basic.csv' and 'advanced.csv'
    by reading a list of words from the file specified by the constant
    COMMON, BASIC, AND ADVANCED, respectively.

    @param  file    the constant name of the file
    returns info
    """
    word = {}
    num = 0

    for line in open(file, encoding="ISO-8859-1"):
        value = ""
        count = 0
        line.strip()
        for term in line.split():
            if count != 0:
                value += term + " "
            else:
                key = term
            count += 1
        word[num] = (key, value)
        num += 1

    return word


def get_word(word, info):
    """
    @param  word
    @param  info     A lexicon list with the word name as a key and
                        the meaning as a value
    returns a list contains the secret word and it's definition
    """
    index = random.randrange(len(word) + 1)
    chosen = word.get(index)  # Gets the word
    player_word = len(chosen[0]) * "-"

    info['answer'] = chosen[0]
    info['input'] = player_word
    info['used'] = ""
    info['tips'] = chosen[1]
    print(chosen)

    return info


