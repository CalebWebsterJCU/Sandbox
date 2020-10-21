"""
Hangman Extreme
something/something/2020
It's hangman. EXTREME!!!
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
import random

GREEN = (0, 1, 0, 1)
RED = (1, 0, 0, 1)
WHITE = (1, 1, 1, 1)


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
/      |
_______|""",
        r"""========
 |     |
 O     |
/|\    |
/ \    |
_______|""",
    ]
    hint_button_text = StringProperty()
    revealed_word = StringProperty()
    gallows = StringProperty()
    guess_info = StringProperty()
    game_result = StringProperty()
    game_info = StringProperty()
    invalid_input_text = StringProperty()

    def __init__(self, **kwargs):
        """Initialize the HangmanExtreme class."""
        super().__init__(**kwargs)
        self.word = ""
        self.correct_letters = []
        self.num_of_incorrect_guesses = 0
        self.guessed_letters = []
        self.num_of_hints_left = 0
        self.game_result = "Hangman EXTREME"
        self.game_info = "Let's Play!"

    def build(self):
        """Create the GUI."""
        self.root = Builder.load_file("hangman_extreme_app.kv")
        self.title = "Hangman Extreme"
        Window.size = (800, 600)
        return self.root

    def handle_start_game(self):
        """Start a new game, setting word and hints to inputs."""
        word = self.root.ids.word_input_box.text
        num_of_hints = self.root.ids.hints_input_box.text
        if word and num_of_hints:
            try:
                num_of_hints = int(num_of_hints)
                if num_of_hints < 0:
                    self.invalid_input_text = "Number must be > 0"
                else:
                    self.word = word
                    self.correct_letters = ["_ " for _ in self.word]
                    if " " in self.word:
                        self.reveal_letters(" ")
                    self.revealed_word = "".join(self.correct_letters)
                    self.num_of_incorrect_guesses = 0
                    self.guessed_letters = []
                    self.num_of_hints_left = num_of_hints
                    self.hint_button_text = "Use Hint\n({} left)".format(self.num_of_hints_left)
                    self.guess_info = ""
                    self.root.ids.screen_manager.transition.direction = "left"
                    self.root.ids.screen_manager.current = "game_screen"
                    self.clear_widget_text(self.root.ids.word_input_box,
                                           self.root.ids.hints_input_box,
                                           self.root.ids.game_info_box,
                                           self.root.ids.gallows_box)
                    self.invalid_input_text = ""
            except ValueError:
                self.invalid_input_text = "Invalid input; enter a valid number"
        else:
            self.invalid_input_text = "All fields must be completed"

    def handle_guess(self):
        """Take a user's guess. If correct, reveal the guessed letters.
        If not, advance the hangman's gallows and noose."""
        guess = self.root.ids.guess_input_box.text.upper()
        self.root.ids.guess_info_box.color = WHITE
        if guess == "":
            self.guess_info = "Invalid guess!"
        elif guess in self.guessed_letters:
            self.guess_info = "Already guessed that letter!"
        else:
            if guess in self.word:
                self.root.ids.guess_info_box.color = GREEN
                self.guess_info = "Correct Guess!"
                self.reveal_letters(guess)
            else:
                self.guessed_letters.append(guess)
                self.root.ids.guess_info_box.color = RED
                self.guess_info = "Incorrect Guess!"
                self.num_of_incorrect_guesses += 1
                self.gallows = self.GALLOWS_STAGES[self.num_of_incorrect_guesses - 1]
                if self.num_of_incorrect_guesses == self.MAX_INCORRECT_GUESSES:
                    self.game_result = "You Lost!"
                    self.root.ids.game_result_box.color = RED
                    self.root.ids.screen_manager.transition.direction = "right"
                    self.root.ids.screen_manager.current = "start_screen"
                    self.game_info = "The word was {}!".format(self.word)

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

    @staticmethod
    def capitalize_input(instance):
        """Capitalizes the input of a text box as it's being typed."""
        instance.text = instance.text.upper()

    @staticmethod
    def limit_characters(instance, num_of_characters):
        """Automatically capitalize letters entered and prevent
        more than a certain number of characters from being entered."""
        if instance.text:
            instance.text = instance.text[num_of_characters - 1]

    @staticmethod
    def allow_certain_characters(instance, allowed_chars="AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz "):
        """Only allow certain characters to be entered."""
        for char in instance.text:
            if char not in allowed_chars:
                instance.text = instance.text[:-1]

    @staticmethod
    def clear_widget_text(*widgets):
        """Clear a specified input box."""
        for widget in widgets:
            widget.text = ""

    def reveal_letters(self, letter):
        """Reveal the letters by changing "_" to the correct letter."""
        self.guessed_letters.append(letter)
        for x in range(len(self.word)):
            if self.word[x] == letter:
                self.correct_letters[x] = letter
                self.revealed_word = "".join(self.correct_letters)
        if self.revealed_word == self.word:
            self.game_result = "You Won!"
            self.root.ids.game_result_box.color = GREEN
            self.game_info = "You guessed \"{}\" in {} tries!".format(
                self.word, len(self.guessed_letters))
            self.root.ids.screen_manager.transition.direction = "right"
            self.root.ids.screen_manager.current = "start_screen"


HangmanExtreme().run()
