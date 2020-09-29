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

CURRENT_DATE_TIME = d.now()
CURRENT_DATE = CURRENT_DATE_TIME.day, CURRENT_DATE_TIME.month, CURRENT_DATE_TIME.year
MONTHS_DICT = {1: 31, 2: 28, 3: 31,
               4: 30, 5: 31, 6: 30,
               7: 31, 8: 31, 9: 30,
               10: 31, 11: 30, 12: 31}


class AgeCalculator(App):
    """Age calculator app that calculates age and total days lived."""
    age_output_text = StringProperty()
    welcome_message = """Welcome to Caleb Webster's Fantastic Age Calculator!
Please enter your date of birth (in slash format) to get started."""
    separator = "/"

    def build(self):
        """Load GUI code from kv file."""
        self.root = Builder.load_file("age_calculator_app.kv")
        self.title = "Age Calculator"
        Window.size = (600, 210)
        return self.root

    def handle_calculate_age(self):
        """Calculate and display exact age and days lived."""
        day, month, year = self.get_valid_date()
        total_days_lived = calc_total_days(CURRENT_DATE) - calc_total_days((day, month, year))
        years, months, days = calc_exact_age(total_days_lived)
        self.age_output_text = f"You are {years} years, {months} months, and {days} days old.\nToday is your {total_days_lived + 1}{find_ordinal(total_days_lived + 1)} day on earth."

    def get_valid_date(self):
        """Get date, returning default date if it is invalid."""
        default_date = CURRENT_DATE
        months_dict = {1: 31, 2: 29, 3: 31, 4: 30, 5: 31, 6: 30,
                       7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
        try:
            date_string = self.root.ids.date_input_box.text
            parts = [int(part) for part in date_string.split(self.separator)]
            day, month, year = parts[0], parts[1], parts[2]
            if year >= 0 and 0 < month <= 12 and 0 < day <= months_dict[month]:
                return day, month, year
            else:
                return default_date
        except ValueError:
            return default_date
        except IndexError:
            return default_date


def is_leap_year(year):
    """Determine if a year is a leap year."""
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


def calc_total_days(date=(1, 1, 2000)):
    """Convert date to total days since 0 A.D.
    Date passed in must be tuple in form (day, month, year)."""
    total_days = 1  # Starting from Jan 1st, 0 A.D
    day, month, year = date[0], date[1], date[2]
    for year_to_add in range(1, year):
        if is_leap_year(year_to_add):
            total_days += 366
        else:
            total_days += 365
    for month_to_add in range(1, month):
        if month_to_add == 2 and is_leap_year(year):
            total_days += 29
        else:
            total_days += MONTHS_DICT[month_to_add]
    total_days += day
    return total_days


def calc_exact_age(total_days):
    """Given total days lived, calculate and return exact age."""
    years = int(total_days // 365.2425)
    total_days %= 365.2425
    months = int(total_days // 30.4167)
    total_days %= 30.4167
    days = int(total_days)
    return years, months, days


def find_ordinal(number):
    """Return the ordinal of a number."""
    special_ordinals = {1: "st", 2: "nd", 3: "rd"}
    last_digit = int(str(number)[-1])
    return special_ordinals[last_digit] if last_digit in special_ordinals else "th"


AgeCalculator().run()
