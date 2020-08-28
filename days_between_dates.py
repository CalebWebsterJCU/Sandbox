"""This program takes a date and calculates how many days since Jan 1, 2000"""

from datetime import datetime as d
CURRENT_DATE = d.now()
CURRENT_DATE_STRING = f"{CURRENT_DATE.day:02}/{CURRENT_DATE.month:02}/{CURRENT_DATE.year}"
MONTHS_DICT = {1: 31, 2: 28, 3: 31,
               4: 30, 5: 31, 6: 30,
               7: 31, 8: 31, 9: 30,
               10: 31, 11: 30, 12: 31}


def main():
    """Take 2 dates and calculate the number of days between them."""
    birth_date_string = get_valid_date_string("Birth Date: ")
    total_days_lived = convert_date_to_days(CURRENT_DATE_STRING) - convert_date_to_days(birth_date_string)
    years, months, days = calc_exact_age(total_days_lived)
    print(f"Today is your {total_days_lived}{find_ordinal(total_days_lived)} day on earth.")
    print(f"You are {years} years, {months} months, and {days} days old.")


def convert_date_to_days(date_string: str) -> int:
    """Convert date to total days since 0 A.D."""
    total_days = 1  # Starting from Jan 1st, 0 A.D
    day, month, year = convert_date_string(date_string)
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


def get_valid_date_string(prompt: str) -> str:
    """Get a valid date string input eg. '01/01/2000'"""
    date_string = ""
    is_valid = False
    while not is_valid:
        try:
            date_string = input(prompt)
            day, month, year = convert_date_string(date_string)
            if year not in range(1, CURRENT_DATE.year + 1) or month not in range(1, 13) or day not in range(1, 32):
                print("Invalid date")
            else:
                is_valid = True
        except ValueError:
            print("Invalid date")
        except IndexError:
            print("Invalid date")
    return date_string


def convert_date_string(date_string: str) -> tuple:
    """Convert date string to day, month and year."""
    date_list = [int(part) for part in date_string.split('/')]
    day, month, year = date_list[0], date_list[1], date_list[2]
    return day, month, year


def is_leap_year(year):
    """Determine if a given year is a leap year."""
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                is_leap = True
            else:
                is_leap = False
        else:
            is_leap = True
    else:
        is_leap = False
    return is_leap


def calc_exact_age(total_days: int):
    """Calculate exact age, given total days lived."""
    years = int(total_days // 365.2425)
    total_days %= 365.2425
    months = int(total_days // 30.4167)
    total_days %= 30.4167
    days = int(total_days)
    return years, months, days


def find_ordinal(number):
    """Given a number, find the ordinal."""
    last_digit = number % 10

    if last_digit == 1:
        ordinal = "st"
    elif last_digit == 2:
        ordinal = "nd"
    elif last_digit == 3:
        ordinal = "rd"
    else:
        ordinal = "th"

    return ordinal


main()
