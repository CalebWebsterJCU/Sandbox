"""
Time Slot
24/10/2020
This class represents a set of two times of day which form a time interval with a start and end time.
Times are military time strings and can be converted to minutes e.g. "15:00" -> 900 minutes
attributes: self.start_time, self.end_time
methods: self.calc_interval(), self.is_after_noon(), self.is_work_hours(), self.convert_to_minutes()
"""

from military_time import MilitaryTime

WORK_HOURS = ("9:00", "17:00")  # 9am to 5pm


class TimeSlot:
    """Represent a military time interval with a start and end time."""

    def __init__(self, start_time=MilitaryTime(), end_time=MilitaryTime()):
        """
        Initialize TimeSlot class, setting start_time and end_time.
        start_time and end_time must be strings
        """
        self.start_time = start_time
        self.end_time = end_time
        self.times = (self.start_time, self.end_time)

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
        """
        return self.start_time.total_minutes, self.end_time.total_minutes


if __name__ == '__main__':
    time_slot1 = TimeSlot(MilitaryTime("10:00"), MilitaryTime("15:00"))
    print(time_slot1)