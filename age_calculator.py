"""
Caleb Webster's Fantastic Age Calculator
something/something/2020
This program calculates your exact age and how many days you've been alive.
"""

from datetime import datetime as d

BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
END = '\033[0m'

CURRENT_DATE = d.now()
CURRENT_DATE_STRING = f"{CURRENT_DATE.day:02}/{CURRENT_DATE.month:02}/{CURRENT_DATE.year}"
MONTHS_DICT = {1: 31, 2: 28, 3: 31,
               4: 30, 5: 31, 6: 30,
               7: 31, 8: 31, 9: 30,
               10: 31, 11: 30, 12: 31}


def main():
    """Get user's birth date, then calculate and display
    user's exact age and the number of days they have lived."""
    print("Welcome to Caleb Webster's Fantastic Age Calculator!")
    print("Please enter your date of birth (in slash format) to get started.")
    birth_date_string = get_valid_date_string(">>> ")
    # Find total days between two dates (birth date and current date)
    total_days_lived = convert_date_to_days(convert_date_string(CURRENT_DATE_STRING, "/")) - convert_date_to_days(convert_date_string(birth_date_string, "/"))
    # Calculate exact age
    years, months, days = calc_exact_age(total_days_lived)
    print(f"You are {years} years, {months} months, and {days} days old.")
    print(f"Today is your {total_days_lived + 1}{find_ordinal(total_days_lived + 1)} day on earth.")


def convert_date_to_days(date):
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


def get_valid_date_string(prompt):
    """Get a valid date string input eg. '01/01/2000'"""
    date_string = ""
    is_valid = False
    while not is_valid:
        try:
            date_string = input(prompt)
            day, month, year = convert_date_string(date_string, "/")
            if year not in range(1, CURRENT_DATE.year + 1) or month not in range(1, 13) or day not in range(1, 32):
                print("Invalid date")
            else:
                is_valid = True
        except ValueError:
            print("Invalid date")
        except IndexError:
            print("Invalid date")
    return date_string


def convert_date_string(date_string, separator):
    """Return day, month, and year of date string."""
    date_list = [int(part) for part in date_string.split(separator)]
    day, month, year = date_list[0], date_list[1], date_list[2]
    return day, month, year


def is_leap_year(year):
    """Determine if a year is a leap year."""
    return year % 4 == 0 and year % 100 != 0 or year % 400 == 0


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
    if last_digit in special_ordinals:
        return special_ordinals[last_digit]
    else:
        return "th"


main()
