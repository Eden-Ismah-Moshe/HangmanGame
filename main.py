# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
import PIL
from PIL import ImageTk, Image

SECRET_WORD = ""
HANGMAN_ASCII_ART = """Welcome to the game Hangman 
      The maximum number of failed attempts allowed in the game is: 6"""
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

def hangman_situation(num_of_tries):
    """Return hangman state, according to input number.
       :param: num_of_tries: define the state to be displayed
       :type: int
       """
    return HANGMAN_PHOTOS[num_of_tries]

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

def clear_screen(window):
    # Destroy all widgets in the window
    for widget in window.winfo_children():
        widget.destroy()

def get_data(window):
    clear_screen(window)

    file_label = tk.Label(window, text="Enter file path:", font=('Helvetica', 11))
    file_label.pack()

    file_entry = tk.Entry(window)
    file_entry.pack()

    number_label = tk.Label(window, text="Enter a number representing the position of a particular word in the file:", font=('Helvetica', 11))
    number_label.pack()

    number_entry = tk.Entry(window)
    number_entry.pack()

    #use a lambda function to delay the execution of the save_data function until the button is clicked
    save_button = tk.Button(window,text="Save Data", command=lambda: save_data(window, file_entry.get(), number_entry.get()), font=('Helvetica', 11))
    save_button.pack()

def save_data(window, file_path ,word_index):
    num_of_tries = 1
    old_letters_guessed = []
    try:
        word_index = int(word_index)
        secret_word = list(choose_word(file_path, word_index))
        start_the_game(window, secret_word, num_of_tries, old_letters_guessed)
    except ValueError:
        # Handle the case where word_index is not a valid integer
        print("Invalid input. Please enter a valid integer for word index.")

def  start_the_game(window, secret_word, num_of_tries, old_letters_guessed):
    clear_screen(window)
    word_label = tk.Label(window, text=show_hidden_word(secret_word, old_letters_guessed), font=('Helvetica', 11))
    word_label.pack(pady=10)
    hangman_label = tk.Label(window, text=hangman_situation(num_of_tries), font=('Helvetica', 11), justify=tk.LEFT, wraplength=200)
    hangman_label.pack(pady=10)

    if num_of_tries <= MAX_TRIES and not check_win(secret_word, old_letters_guessed):
        input_char_label = tk.Label(window, text="Please guess a letter: ", font=('Helvetica', 11))
        input_char_label.pack()
        input_char = tk.Entry(window)
        input_char.pack()

        save_button = tk.Button(window, text="Save Guess",
                                command=lambda: guess_of_letter(window, secret_word, num_of_tries, input_char.get(), old_letters_guessed) if input_char.get() != "" else None, font=('Helvetica', 11))
        save_button.pack()
        window.update()  #Update the window to show the widgets
        window.wait_window(window) #Wait for the user to click the Save Guess button

        # After the dialog is closed, clear the widgets
        input_char_label.pack_forget()
        input_char.pack_forget()
        save_button.pack_forget()
    else:
        clear_screen(window)
        if check_win(secret_word, old_letters_guessed) == True:
            game_over = "YOU WIN"
        else:
            game_over = "YOU LOSE"
        game_over_label = tk.Label(window, text=game_over, font=('Helvetica', 11))
        game_over_label.pack(pady=10)

def guess_of_letter(window, secret_word, num_of_tries, input_char, old_letters_guessed):
    valid_char = try_update_letter_guessed(input_char, old_letters_guessed)
    if valid_char == True:
        clear_screen(window)
        word_label = tk.Label(window, text=show_hidden_word(secret_word, old_letters_guessed), font=('Helvetica', 11))
        word_label.pack(pady=10)

    char_in_word = False
    for word in secret_word:
        if input_char.lower() in word.lower():
            char_in_word = True
            break
    if (valid_char == True) and (char_in_word == False):
        guess_label = tk.Label(window, text="Wrong Guess :( ", font=('Helvetica', 11))
        guess_label.pack(pady=10)
        num_of_tries += 1
        hangman_label = tk.Label(window, text=hangman_situation(num_of_tries), font=('Helvetica', 11), justify=tk.LEFT, wraplength=200)
        hangman_label.pack(pady=10)
    else:
        guess_label = tk.Label(window, text="Good Guess :) ", font=('Helvetica', 11))
        guess_label.pack(pady=10)

    continue_button = tk.Button(window, text="Continue",
                            command=lambda: start_the_game(window, secret_word, num_of_tries, old_letters_guessed), font=('Helvetica', 11))
    continue_button.pack()

def main():
    #Creating the window
    window = tk.Tk()
    window.title("Hangman Game")

    # Creating a Label widget to display the question
    label_of_main_screen = tk.Label(window, text=HANGMAN_ASCII_ART, font=('Helvetica', 11))
    label_of_main_screen.pack(pady=10)

    # Opening and converting the image to a PhotoImage object
    original_image = Image.open("C:/Networks/HangmanGame/logo.jpg")
    resized_image = original_image.resize((500, 150), PIL.Image.Resampling.LANCZOS)

    # Converting the resized image to a PhotoImage object
    window.photo = ImageTk.PhotoImage(resized_image)

    # Creating a Button widget with an image
    button_start_play = tk.Button(window, image=window.photo, command=lambda: get_data(window))
    button_start_play.pack(pady=20)

    # Creating a Button widget to create the button
    button_start_play = tk.Button(window, text="click to start play!", command=lambda: get_data(window), font=('Helvetica', 11))
    button_start_play.pack(pady=20)

    # Displaying the window
    window.mainloop()

if __name__ == "__main__":
    main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/