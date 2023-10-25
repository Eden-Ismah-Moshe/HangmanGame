# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import random

HANGMAN_ASCII_ART = """Welcome to the game Hangman 
        _    _    
       | |  | |   
       | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __
       |  __  |/ _' | '_ \ / _' | '_ ' _ \ / _' | '_ \ 
       | |  | | (_| | | | | (_| | | | | | | (_| | | | |
       |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                        __/ |
                       |___/ """
MAX_TRIES = 6
NOT_UPDATED_STR = "X\n{0}"
HANGMAN_PHOTOS = {1: "x-------x",
                  2: """
                    x-------x
                    |
                    |
                    |
                    |
                    |
                    """,
                  3: """
                    x-------x
                    |       |
                    |       0
                    |
                    |
                    |
                    """,
                  4: """
                    x-------x
                    |       |
                    |       0
                    |       |
                    |
                    |
                    """,
                  5: """
                    x-------x
                    |       |
                    |       0
                    |      /|\\
                    |
                    |
                """,
                  6: """
                    x-------x
                    |       |
                    |       0
                    |      /|\\
                    |      /
                    |
                """,
                  7: """
                    x-------x
                    |       |
                    |       0
                    |      /|\\
                    |      / \\
                    |
                """}

def check_valid_input(letter_guessed, old_letters_guessed):
    """Checks the validation of user input, e.g one English letter, not entered
       before
       :param letter_guessed: user input
       :param old_letters_guessed: previous inputs
       :type letter_guessed: string
       :type old_letters_guessed: list
       :return: True if input is valid, False if not.
       :rtype: boolean
       """
    if (len(letter_guessed) > 1):
        print("Error! You entered more than one character.")
        return False
    elif not letter_guessed.isalpha():
        print("Error! The character you entered is not an English letter.")
        return False
    elif letter_guessed.lower() in old_letters_guessed:
        print("Error! You've already guessed this character before.")
        return False
    else:
        return True

def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """Checks validation of user’s input (as in previous task).
        if so, adds it to "old_letters_guessed" and returns True. Otherwise returns
        False.
        :param letter_guessed: user’s input
        :param old_letters_guessed: previous (valid) inputs
        :type letter_guessed: string
        :type old_letters_guessed: list
        :return: True if input is valid, False if not.
        :rtype: boolean
    	"""
    if check_valid_input(letter_guessed, old_letters_guessed) == True:
        old_letters_guessed += letter_guessed.lower()
        return True
    else:
        print_list_not_updated(old_letters_guessed)
        return False

def print_list_not_updated(my_list):
    """Prints not-ypdated string.
        :param my_list (not updates)
        :type my_list: list
        """
    print(NOT_UPDATED_STR.format(" -> ".join(sorted(my_list))))

def show_hidden_word(secret_word, old_letters_guessed):
    """Displays guessed letters in the secret word, and '_' for letters that were
    not guessed yet
    :param: secret_word: the word to be guessed
    :param: old_lettes_guessed: the letters that were guessted (user's input)
    :type secret_word: list
    :type old_lettes_guessed: list
    :return: the updated list, with all guessed letters
    :rtype: list
    """
    str = ""
    for letter in secret_word:
        if letter in old_letters_guessed:
            str += (letter + ' ')
        else:
            str += "_ "
    return str[:-1]

def check_win(secret_word, old_letters_guessed):
    """Checks if the whole secret word was guested correctly
   	:param: secret_word: the word to be guessed
    :param: old_letters_guessed: the letters that were guested (user's input)
    :type secret_word: list
    :type old_lettes_guessed: list
    :return: True if the secret word was guessed, False if not
    :rtype: boolean
    """
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True

def print_hangman(num_of_tries):
    """Prints hangman state, according to input number.
       :param: num_of_tries: define the state to be displayed
       :type: int
       """
    print(HANGMAN_PHOTOS[num_of_tries])

def choose_word(file_path, index):
    """Picks one word from a list of words, read from a file, according to a given index in the list
    :param: file_path: the path of the file that contains a word list
    :param: index: the position of the word to be picked
    :type: file_path: string
    :type: index: int
    :return: the picked word
    :rtype: string
    """
    with open(file_path, 'r') as words:
        word_list = words.read().split(' ')
    i = (index - 1) % len(word_list)
    return word_list[i]

def main():
    print(HANGMAN_ASCII_ART)
    print("The maximum number of failed attempts allowed in the game is: %d" % MAX_TRIES)
    num_of_tries = 1
    old_letters_guessed = []

    file_path = input("Enter file path: ")
    word_index = int(input("Enter a number representing the position of a particular word in the file: "))

    secret_word = list(choose_word(file_path, word_index))
    print_hangman(num_of_tries)
    print(show_hidden_word(secret_word, old_letters_guessed))


    while (num_of_tries <= MAX_TRIES) and (check_win(secret_word, old_letters_guessed)==False):
        input_char = input("Please enter one character: ")
        valid_char = try_update_letter_guessed(input_char, old_letters_guessed)
        if valid_char==True:
            print(show_hidden_word(secret_word, old_letters_guessed))

        char_in_word = False
        for word in secret_word:
            if input_char.lower() in word.lower():
                char_in_word = True
                break
        if (valid_char==True) and (char_in_word==False):
            print("Wrong Guess :( ")
            num_of_tries += 1
            print_hangman(num_of_tries)
        else:
            print("Good Guess :) ")


    if check_win(secret_word, old_letters_guessed)==True:
        print("YOU WIN")
    else:
        print("YOU LOSE")


if __name__ == "__main__":
    main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/