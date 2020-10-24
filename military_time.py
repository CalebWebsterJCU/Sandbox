"""
Military Time
24/10/2020
Represents a military time of day e.g. 13:00
Time is a string and can be represented in total minutes, e.g. "00:00" -> 0 minutes, "10:00" -> 600 minutes
attributes: self.time, self.minutes
methods: comparisons (__lt__(), __add__(), etc.), is_work_hours(), conv_to_standard()
"""

WORK_HOURS = ("9:00", "17:00")  # 9am to 5pm


class Time:
    """
    Represent military time object with string and minutes.
    Time must be passed in as a string
    attributes: self.time, self.minutes
    methods: comparisons (__lt__(), __add__(), etc.), is_work_hours(), conv_to_standard()
    """

    def __init__(self, time="00:00"):
        """
        Create time object, setting time, hour, minute, total_minutes, is_after_noon, and is_valid.
        :param time: military time string, e.g. "15:00"
        """
        self.hour, self.minute = [int(part) for part in time.split(":")]
        self.time = f"{self.hour:02}:{self.minute:02}"
        self.total_minutes = self.hour * 60 + self.minute
        self.is_after_noon = self.total_minutes >= 720
        self.is_valid = 0 <= self.total_minutes < 1440

    def __str__(self):
        """
        Define rules for printing time objects.
        :return: "{self.hour:02}:{self.minute:02}"
        """
        return f"{self.hour:2}:{self.minute:02}"

    def __repr__(self):
        """
        Define rules for displaying time objects in a list.
        :return: "{self.hour:2}:{self.minute:02}"
        """
        return f"{self.hour:2}:{self.minute:02}"

    def __lt__(self, other):
        """
        Compare self to other time object, returning True if self comes before other, e.g. "01:00" < "02:00"
        :param other: time object to compare self to
        :return: True or False
        """
        return self.total_minutes < other.total_minutes

    def __gt__(self, other):
        """
        Compare self to other time object, returning True if self comes after other, e.g. "02:00" > "01:00"
        :param other: time object to compare self to
        :return: True or False
        """
        return self.total_minutes > other.total_minutes

    def __eq__(self, other):
        """
        Compare self to other time object, returning True if self is equal to other, e.g. "01:00" == "01:00"
        :param other: time object to compare self to
        :return: True or False
        """
        return self.total_minutes == other.total_minutes

    def __le__(self, other):
        """
        Compare self to other time object, returning True if self comes before or is equal to other, e.g. "02:00" <= "02:00"
        :param other: time object to compare self to
        :return: True or False
        """
        return self.total_minutes <= other.total_minutes

    def __ge__(self, other):
        """
        Compare self to other time object, returning True if self comes after or is equal to other, e.g. "01:00" >= "01:00"
        :param other: time object to compare self to
        :return: True or False
        """
        return self.total_minutes >= other.total_minutes

    def __sub__(self, other):
        """
        Subtract other time object from self, returning their difference in total minutes.
        :param other: time object to subtract
        :return: difference (int) between two time objects (minutes)
        """
        return self.total_minutes - other.total_minutes

    def __add__(self, other):
        """
        Add other time object to self, returning their sum in total minutes.
        :param other: time object to add
        :return: sum (int) of two time objects (minutes)
        """
        return self.total_minutes + other.total_minutes

    def is_work_hours(self):
        """
        Return True if time is between working hours, False if it is not.
        :return: True or False
        """
        return Time(WORK_HOURS[0]) <= self <= Time(WORK_HOURS[1])

    def conv_to_standard(self):
        """
        Convert military time to standard time, returning standard time string with either "am" or "pm" on the end.
        :return: time string in standard form
        """
        if self.is_valid:
            meridian = "pm" if self.hour >= 12 else "am"
            minutes = self.minute
            hours = self.hour
            if hours >= 12:
                hours %= 12
            if hours == 0:
                hours = 12
            return f"{hours}:{minutes:02}{meridian}"
        return "Invalid time"


if __name__ == '__main__':
    time1 = Time("09:30")
    time2 = Time("10:00")
    time3 = Time("12:00")
    print(time1.time)
    print(time1)
    print(time1.hour, time1.minute)
    print(time1.total_minutes)
    print(time1.is_after_noon)
    print(time3.conv_to_standard())
    assert isinstance(time1.hour, int)
    assert isinstance(time1.minute, int)
    assert isinstance(time1.total_minutes, int)
    assert not time1.is_after_noon
    assert time1 < time2
    assert time2 > time1
    assert time2 - time1 == 30
    assert time1 + time2 == 570 + 600
    assert time2.is_work_hours()
