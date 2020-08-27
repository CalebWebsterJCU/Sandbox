"""This program takes a date and calculates how many days since Jan 1, 2000"""

MONTHS_DICT = {1: 31, 2: 28, 3: 31,
               4: 30, 5: 31, 6: 30,
               7: 31, 8: 31, 9: 30,
               10: 31, 11: 30, 12: 31}


def main():
    """Take 2 dates and calculate the number of days between them."""
    days_between_dates = convert_date_to_days('27/08/2020') - convert_date_to_days('27/05/2001')
    print(days_between_dates)


def convert_date_to_days(date: str) -> int:
    """Convert date to total days since 0 A.D."""
    total_days = 1  # Starting from Jan 1st, 0 A.D
    date_list = [int(part) for part in date.split('/')]
    year = date_list[2]
    month = date_list[1]
    day = date_list[0]
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


main()