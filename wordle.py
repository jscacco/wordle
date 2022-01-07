from colorama import Fore, Back, Style
import enchant

def setup_board(word, guesses):
    """Given a word, return an array which keeps track of guesses and such."""
    placeholder = "_" * len(word)
    return [placeholder for _ in range(guesses)]


def print_board(word, board):
    for guess in board:
        print_formatted_word(word, guess)


def print_formatted_word(word, guess):
    for i in range(len(guess)):
        # Print out the letter in the correct color
        if guess[i].upper()== word[i].upper():
            print(Fore.GREEN + guess[i].upper(), end='')
        elif guess[i].upper() in word:
            print(Fore.YELLOW + guess[i].upper(), end='')
        else:
            print(guess[i].upper(), end='')

        print(Style.RESET_ALL, end='')

        if i < len(guess) - 1:
            print(" ", end='')
        else:
            print()


def print_eliminated(eliminated):
    """Given an array representing eliminated letters, print out those letters in a nice format."""
    this_str = "Eliminated letters: "
    for i in range(len(eliminated)):
        this_str += sorted(eliminated)[i].upper()
        if i < len(eliminated) - 1:
            this_str += ", "
    print(this_str)


def check_word(guess, length, eliminated):
    """Given a guess, return true if it is an english word of correct length and containing no elimiated
        letters."""

    d = enchant.Dict("en_US")
    contains_eliminated = False

    for c in eliminated:
        if c in guess:
            contains_eliminated = True

    return d.check("Hello") and len(guess) == length and not contains_eliminated


def get_random_word(file="5words.txt"):
    """Given a word file, return a random word from that file."""
    words = open(file).read().splitlines()
    pass


def wordle(word, guesses=6):
    """Play wordle!"""

    winner = False
    eliminated = []
    board = setup_board(word, guesses)
    print_board(word, board)

    turn = 0
    while turn < guesses:
        # Display letters that have been eliminated via previous guesses
        if turn > 0:
            print_eliminated(eliminated)

        # Get the next guess, update board, update eliminated
        this_guess = input("Make a guess: ").upper()
        while not check_word(this_guess, len(word), eliminated):
            this_guess = input("Oops! Enter an English word of length " + str(len(word)) + " containing no eliminated letters: ").upper()
        board[turn] = this_guess
        for c in this_guess:
            if c not in word:
                eliminated.append(c.upper())

        # Output the new board, check to see if we have won
        print_board(word, board)
        if this_guess == word:
            turn = guesses
            winner = True
        turn += 1
    
    if winner:
        msg = "Congratulations!"
    else:
        msg = "Sorry, good luck next time! The word was " + word.upper()
    print(msg)


def main1():
    word = "JACK"
    guesses = 6
    board = setup_board(word, guesses)
    wordle(word)

def main():
    word_file = open("/usr/share/dict/words", 'r')
    # f = open("5words.txt", 'a')
    


if __name__ == "__main__":
    main()
    