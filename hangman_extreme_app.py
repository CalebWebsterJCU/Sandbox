"""
Hangman Extreme
something/something/2020
Its hangman.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty


class HangmanExtreme(App):
    """Hangman game in which a user tries to guess
    letters in a word. If they get all the letters,
    they win. Too many guesses, and they get hung."""

    revealed_word = StringProperty()
    gallows = StringProperty()
    guess_info = StringProperty()
    word = "ANTARCTICA"

    def __init__(self, **kwargs):
        """Initialize the HangmanExtreme class."""
        super().__init__(**kwargs)
        self.correct_characters = ["_" for _ in self.word]
        self.revealed_word = "".join(self.correct_characters)
        self.guessed_characters = []

    def build(self):
        """Create the GUI."""
        self.root = Builder.load_file("hangman_extreme_app.kv")
        return self.root

    def handle_guess(self):
        """Take a user's guess. If correct, reveal
        the guessed letters. If not, advance the
        hangman's gallows and noose."""
        guess = self.root.ids.guess_input_box.text.upper()
        if len(guess) > 1 or not guess:
            self.guess_info = "Invalid guess!"
        elif guess in self.guessed_characters:
            self.guess_info = "Already guessed that letter!"
        else:
            self.guessed_characters.append(guess)
            if guess in self.word:
                self.guess_info = "Correct Guess"
                self.reveal_letters(guess)
            else:
                self.guess_info = "Incorrect Guess"

    def reveal_letters(self, guess):
        """Reveal the letters by changing "_" to the correct letter."""
        for x in range(len(self.word)):
            if self.word[x] == guess:
                self.correct_characters[x] = guess
                self.revealed_word = "".join(self.correct_characters)
        if self.revealed_word == self.word:
            pass


HangmanExtreme().run()