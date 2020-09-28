"""
Age Calculator App
something/something/2020
This Kivy app calculates your exact age and how many days you've lived.
"""

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.properties import StringProperty
from datetime import datetime as d


class AgeCalculator(App):
    """Age calculator app that calculates age and total days lived."""
    age_output_text = StringProperty()
    welcome_message = """Welcome to Caleb Webster's Fantastic Age Calculator!
Please enter your date of birth (in slash format) to get started."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        """Load GUI code from kv file."""
        self.root = Builder.load_file("age_calculator_app.kv")
        return self.root



AgeCalculator().run()
