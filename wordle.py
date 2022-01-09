from colorama import Fore, Back, Style
import enchant
import random
ALPHABET = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def setup_board(word, guesses):
    """Given a word, return an array which keeps track of guesses and such."""
    placeholder = "_" * len(word)
    return [placeholder for _ in range(guesses)]


def print_board(word, board):
    for guess in board:
        print_formatted_word(word, guess)


def assign_colors(word, guess):
    """Given a word and a guess, return the colors of each letter in the guess."""
    
    assert len(word) == len(guess)
    length = len(word)
    
    colors = ['_' for _ in range(length)]
    data = {}
    
    # First pass - this will give everything the correct color but may result in too many yellows
    for i in range(length):
        this_guess = guess[i]
        this_word = word[i]
        if this_guess == this_word:
            colors[i] = 'g'
            if this_guess not in data:
                data[this_guess] = {"green": 1, "yellow": 0}
            else:
                data[this_guess]["green"] += 1
        elif this_guess in word:
            colors[i] = 'y'
            if this_guess not in data:
                data[this_guess] = {"green": 0, "yellow": 1}
            else:
                data[this_guess]["yellow"] += 1
        else:
            if this_guess not in data:
                data[this_guess] = {"green": 0, "yellow": 0}
            colors[i] = 'w'


    # Second pass - remove extra yellows
    for i in reversed(range(len(word))):
        if colors[i] == 'y':
            if word.count(guess[i]) < data[guess[i]]['green'] + data[guess[i]]['yellow']:
                colors[i] = 'w'
                data[guess[i]]['yellow'] -= 1

    return colors


def print_formatted_word(word, guess):
    colors = assign_colors(word, guess)
    for i in range(len(guess)):
        if colors[i] == 'g':
            print(Fore.GREEN + guess[i], end='')
        elif colors[i] == 'y':
            print(Fore.YELLOW + guess[i], end='')
        else:
            print(guess[i], end='')

        print(Style.RESET_ALL, end='')

        if i < len(guess) - 1:
            print(" ", end='')
        else:
            print()


def print_eliminated(eliminated):
    """Given an array representing eliminated letters, print out those letters in a nice format."""
    this_str = "Eliminated: "
    for i in range(len(eliminated)):
        this_str += sorted(eliminated)[i]
        if i < len(eliminated) - 1:
            this_str += ", "
    print(this_str)


def print_available(eliminated):
    """Given a list of eliminated letters, print the ones which are still available"""
    output = "Available: "
    for letter in ALPHABET:
        if letter not in eliminated:
            output += letter + ", "
    print(output[:-2])


def check_word(guess, length, eliminated):
    """Given a guess, return true if it is an english word of correct length and containing no elimiated
        letters."""

    d = enchant.Dict("en_US")
    contains_eliminated = False

    for c in eliminated:
        if c in guess:
            contains_eliminated = True

    return d.check("Hello") and len(guess) == length and not contains_eliminated


def get_random_word(file="5words"):
    """Given a word file, return a random word from that file."""
    words = open(file).read().splitlines()
    return random.choice(words).upper()


def wordle(word, guesses=6):
    """Play wordle!"""

    winner = False
    eliminated = set()
    board = setup_board(word, guesses)
    print_board(word, board)

    turn = 0
    while turn < guesses:
        # Display letters that have been eliminated via previous guesses
        if turn > 0:
            print_eliminated(eliminated)
            print_available(eliminated)

        # Get the next guess, update board, update eliminated
        this_guess = input("Make a guess: ").upper()
        while not check_word(this_guess, len(word), eliminated):
            this_guess = input("Oops! Enter an English word of length " + str(len(word)) + " containing no eliminated letters: ").upper()
        board[turn] = this_guess
        for c in this_guess:
            if c not in word:
                eliminated.add(c)

        # Output the new board, check to see if we have won
        print_board(word, board)
        if this_guess == word:
            turn = guesses
            winner = True
        turn += 1
    
    if winner:
        msg = "Congratulations!"
    else:
        msg = "Sorry, good luck next time! The word was " + word
    print(msg)


def main():
    word = get_random_word()
    guesses = 6
    board = setup_board(word, guesses)
    wordle(word)


if __name__ == "__main__":
    main()
    