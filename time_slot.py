"""
Time Slot
24/10/2020
This class represents a set of two times of day which form a time interval with a start and end time.
Times are military time strings and can be converted to minutes e.g. "15:00" -> 900 minutes
attributes: self.start_time, self.end_time
methods: conv_to_min(), is_work_hours(), is_after_noon(), calc_interval(), conv_to_standard(), is_valid()
"""

from military_time import MilitaryTime

WORK_HOURS = ("9:00", "17:00")  # 9am to 5pm


class TimeSlot:
    """
    Represent a military time interval with a start and end time.
    Times must be objects of Time class
    attributes: self.start_time, self.end_time
    methods: conv_to_min(), is_work_hours(), is_after_noon(), calc_interval(), conv_to_standard(), is_valid()
    """

    def __init__(self, start_time=MilitaryTime(), end_time=MilitaryTime()):
        """
        Initialize TimeSlot class, setting start_time and end_time.
        start_time and end_time must be strings
        """
        self.start_time = start_time
        self.end_time = end_time

    def __str__(self):
        """
        Specify rules for printing time slots.
        :return: "{self.start_time} - {self.end_time}"
        """
        return f"{self.start_time} - {self.end_time}"

    def conv_to_min(self):
        """
        If reverse = False, convert military time string to a number of minutes.
        If reverse = True, Convert a number of minutes to a military time string.
        Time strings must be in military time format e.g. 15:00 (no seconds)
        Number of minutes must be an integer
        :return: tuple of start_time.minutes & end_time.minutes
        """
        return self.start_time.total_minutes, self.end_time.total_minutes

    def is_work_hours(self):
        """
        Return True if start_time and end_time are in work hours, False if one or both are not.
        :return: True or False
        """
        return self.start_time.is_work_hours() and self.end_time.is_work_hours()

    def is_after_noon(self):
        """
        Return True if start_time and end_time are after 12:00, False if they is not.
        :return: True or False
        """
        return self.start_time.is_after_noon and self.end_time.is_after_noon

    def calc_interval(self):
        """
        Calculate and return the difference between the two dates (last minus first) in minutes
        :return: end_time - start_time
        """
        return self.end_time - self.start_time

    def conv_to_standard(self):
        """
        Return time slot with times converted to standard times instead of military.
        :return: Time slot with start_time and end_time converted to standard form
        """
        if self.is_valid():
            return f"{self.start_time.conv_to_standard()} - {self.end_time.conv_to_standard()}"
        return "Invalid time slot"

    def is_valid(self):
        """
        Return True if time slot is valid, False if it is not.
        Time slot is valid if both times are valid and end time is greater than end time.
        :return: True or False
        """
        return self.start_time.is_valid and self.end_time.is_valid and self.end_time > self.start_time


if __name__ == '__main__':
    time_slot1 = TimeSlot(MilitaryTime("10:00"), MilitaryTime("15:00"))
    assert isinstance(time_slot1.start_time, object)
    assert isinstance(time_slot1.end_time, object)
    print(time_slot1)
    assert time_slot1.is_work_hours()
    assert not time_slot1.is_after_noon()
    assert time_slot1.calc_interval() == 300
    print(time_slot1.conv_to_standard())
    assert time_slot1.is_valid()

