"""
Hangman Extreme
something/something/2020
Its hangman. EXTREME!!!
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
import random

WORDS_FILE = "words.txt"


class HangmanExtreme(App):
    """Hangman game in which a user tries to guess
    letters in a word. If they get all the letters,
    they win. Too many guesses, and they get hung."""
    MAX_INCORRECT_GUESSES = 10
    GALLOWS_STAGES = [
        r"""        
        
        
        
        
_______ """,
        r"""        
       |
       |
       |
       |
_______|""",
        r"""========
       |
       |
       |
       |
_______|""",
        r"""========
 |     |
       |
       |
       |
_______|""",
        r"""========
 |     |
 O     |
       |
       |
_______|""",
        r"""========
 |     |
 O     |
 |     |
       |
_______|""",
        r"""========
 |     |
 O     |
/|     |
       |
_______|""",
        r"""========
 |     |
 O     |
/|\    |
       |
_______|""",
        r"""========
 |     |
 O     |
/|\    |
       |
_______|""",
        r"""========
 |     |
 O     |
/|\    |
/      |
_______|""",
        r"""========
 |     |
 O     |
/|\    |
/ \    |
_______|"""
    ]
    hint_button_text = StringProperty()
    revealed_word = StringProperty()
    gallows = StringProperty()
    guess_info = StringProperty()
    game_result = StringProperty()
    game_info = StringProperty()

    def __init__(self, **kwargs):
        """Initialize the HangmanExtreme class."""
        super().__init__(**kwargs)
        self.word = choose_random_word(WORDS_FILE)
        self.correct_letters = ["_ " for _ in self.word]
        self.num_of_incorrect_guesses = 0
        self.revealed_word = "".join(self.correct_letters)
        self.guessed_letters = []
        self.reveal_letters(" ")
        self.num_of_hints_left = 3
        self.hint_button_text = "Use Hint\n({} left)".format(self.num_of_hints_left)

    def build(self):
        """Create the GUI."""
        self.root = Builder.load_file("hangman_extreme_app.kv")
        self.title = "Hangman Extreme"
        self.root.ids.screen_manager.current = "game_screen"
        Window.size = (800, 600)
        return self.root

    def handle_guess(self):
        """Take a user's guess. If correct, reveal the guessed letters.
        If not, advance the hangman's gallows and noose."""
        guess = self.root.ids.guess_input_box.text.upper()
        self.clear_guess_input_box()
        if len(guess) > 1 or not guess:
            self.guess_info = "Invalid guess!"
        elif guess in self.guessed_letters:
            self.guess_info = "Already guessed that letter!"
        else:
            if guess in self.word:
                self.guess_info = "Correct Guess"
                self.reveal_letters(guess)
            else:
                self.guess_info = "Incorrect Guess"
                self.num_of_incorrect_guesses += 1
                self.gallows = self.GALLOWS_STAGES[self.num_of_incorrect_guesses - 1]
                if self.num_of_incorrect_guesses == self.MAX_INCORRECT_GUESSES:
                    self.game_result = "You Lost!"
                    self.root.ids.game_result_box.color = (1, 0, 0, 1)
                    self.root.ids.screen_manager.transition.direction = "left"
                    self.root.ids.screen_manager.current = "end_screen"

    def handle_use_hint(self):
        """Consume one of the player's hints, revealing a random correct letter."""
        if self.num_of_hints_left > 0:
            possible_hint_letters = [letter for letter in self.word if
                                     letter not in self.guessed_letters]
            hint_letter = random.choice(possible_hint_letters)
            self.reveal_letters(hint_letter)
            self.num_of_hints_left -= 1
            self.hint_button_text = "Use Hint\n({} left)".format(self.num_of_hints_left)
            self.guess_info = "Hint used! You have {} left".format(self.num_of_hints_left)
        else:
            self.guess_info = "No more hints left!"

    def control_input(self):
        """Automatically capitalize letters entered and prevent
        more than one character from being entered."""
        if self.root.ids.guess_input_box.text:
            self.root.ids.guess_input_box.text = self.root.ids.guess_input_box.text[0].upper()
        else:
            self.root.ids.guess_input_box.text = self.root.ids.guess_input_box.text.upper()

    def clear_guess_input_box(self):
        """Clear the guess input box so that another letter can be entered."""
        self.root.ids.guess_input_box.text = ""

    def reveal_letters(self, letter):
        """Reveal the letters by changing "_" to the correct letter."""
        self.guessed_letters.append(letter)
        for x in range(len(self.word)):
            if self.word[x] == letter:
                self.correct_letters[x] = letter
                self.revealed_word = "".join(self.correct_letters)
        if self.revealed_word == self.word:
            self.game_result = "You Won!"
            self.root.ids.game_result_box.color = (0, 1, 0, 1)
            self.game_info = "You guessed \"{}\" in {} tries!".format(
                self.word, len(self.guessed_letters))
            self.root.ids.screen_manager.transition.direction = "left"
            self.root.ids.screen_manager.current = "end_screen"

    def reset_game(self):
        """Reset the game, setting a new word and clearing all guesses."""
        self.word = choose_random_word(WORDS_FILE)
        self.correct_letters = ["_ " for _ in self.word]
        if " " in self.word:
            self.reveal_letters(" ")
        self.revealed_word = "".join(self.correct_letters)
        self.num_of_incorrect_guesses = 0
        self.guessed_letters = []
        self.num_of_hints_left = 3
        self.root.ids.screen_manager.current = "game_screen"
        self.root.ids.screen_manager.transition.direction = "right"


def choose_random_word(file_name):
    """Choose and return a random word from a file."""
    words_file = open(file_name, 'r')
    possible_words = words_file.readlines()
    chosen_word = random.choice(possible_words).strip()
    words_file.close()
    print(chosen_word)
    return chosen_word.upper()


HangmanExtreme().run()
