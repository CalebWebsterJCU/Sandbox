"""
meeting_times
23/10/2020
This program takes two peoples' calendars and displays possible time slots during which they can have a meeting.
Times given must be within working hours (9:00 - 17:00)
"""

WORK_START_TIME = "9:00"
WORK_END_TIME = "17:00"
MINIMUM_MEETING_TIME = 30


def convert_time(string_or_minutes, reverse=False):
    """
    If reverse = False, convert military time string to a number of minutes.
    If reverse = True, Convert a number of minutes to a military time string.
    Time strings must be in military time format e.g. 15:00 (no seconds)
    Number of minutes must be an integer
    >>> convert_time("9:00", reverse=False)
    540
    >>> convert_time("17:30", reverse=False)
    1050
    >>> convert_time("-1:00", reverse=False)
    -60
    >>> convert_time(0, reverse=True)
    '00:00'
    >>> convert_time(540, reverse=True)
    '09:00'
    >>> convert_time(-1020, reverse=True)
    '-17:00'
    """
    if reverse:
        hours = string_or_minutes // 60
        minutes = string_or_minutes % 60
        return f"{hours:02}:{minutes:02}"
    else:
        hours, minutes = [int(part) for part in string_or_minutes.split(":")]
        return hours * 60 + minutes


def convert_calendar(calendar, reverse=False):
    """
    Convert calendars of time strings to calendars of minutes.
    Calendars must be lists of time slots (lists with two time strings) e.g. [ ["9:00", "12:30"], ["14:00", "15:30"] ]
    Calendars must be mutable
    >>> convert_calendar([["12:30", "15:00"], ["9:00", "10:30"]], reverse=False)
    ([[750, 900], [540, 630]])
    >>> convert_calendar([[750, 900], [540, 630]], reverse=True)
    ([["12:30", "15:00"], ["9:00", "10:30"]])
    """
    for time_slot in calendar:
        time_slot[0], time_slot[1] = convert_time(time_slot[0], reverse), convert_time(time_slot[1], reverse)
    return calendar


def return_intervals(the_list, step=1):
    """
    Given a list of integers, return a list of intervals.
    Numbers in intervals must be consecutive in list
    Single numbers (numbers with no greater than or less than numbers to the right or left) will be removed
    :param the_list: list of integers sorted in ascending order
    :param step: difference between integers in intervals
    :return: a list of lists containing start and end numbers
    >>> return_intervals([1, 2, 3, 4, 10, 11, 12, 5, 6, 7], 1)
    [[1, 4], [10, 12], [5, 7]]
    >>> return_intervals([-2, 0, 2, 4, 6, 8, 40, 42, 44, 3, 2, 4], 2)
    [[-2, 8], [40, 44], [2, 4]]
    """
    for thing in the_list:
        assert isinstance(thing, int), "List must only contain integers!"
    end_numbers = []
    intervals = []
    for index, number in enumerate(the_list):
        # Check if number is first or last index
        if index == 0 and the_list[index + 1] != number + step:
            if the_list[index + 1] == number + step:
                end_numbers.append(number)
        elif index == len(the_list) - 1:
            if the_list[index - 1] == number - step:
                end_numbers.append(number)
        # Check if number is first or last number in interval
        elif the_list[index - 1] != number - step and the_list[index + 1] == number + step:
            end_numbers.append(number)
        elif the_list[index + 1] != number + step and the_list[index - 1] == number - step:
            end_numbers.append(number)
    for index in range(0, len(end_numbers), 2):
        intervals.append([end_numbers[index], end_numbers[index + 1]])
    return intervals


def main():
    """Convert calendars, then display common available time slots between calendars."""
    all_times = list(range(convert_time(WORK_START_TIME), convert_time(WORK_END_TIME) + 1))
    calendar1 = [["9:00", "16:50"]]
    calendar2 = [["9:00", "16:50"], ["17:00", "17:00"]]
    calendars = [calendar1, calendar2]
    unavailable_times = [convert_calendar(calendar, False) for calendar in calendars]
    for time in all_times.copy():
        for calendar in unavailable_times:
            for time_slot in calendar:
                if time in range(time_slot[0], time_slot[1] + 1):
                    if time in all_times:
                        all_times.remove(time)
    available_times = return_intervals(all_times)
    available_calendar = convert_calendar(available_times, True)
    for available_time in available_calendar:
        print(f"{available_time[0]} - {available_time[1]}")


main()
