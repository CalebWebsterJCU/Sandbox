"""
Day Calendar
24/10/2020
This class represents a person's day calendar, a list of busy time slots for a specific day.
Busy time slots are objects of TimeSlot class which are added to a list.
Attributes: self.name, self.time_slots
Methods: add_time_slot(), remove_time_slot(), conv_to_min(),
is_valid(), load_time_slots(), save_time_slots(), sort_time_slots()
"""

from time_slot import TimeSlot
from military_time import Time


class DayCalendar:
    """
    Represent a person's calendar for a day.
    Items in self.time_slots must be objects of class TimeSlot
    Attributes: self.name, self.time_slots
    Methods: add_time_slot(), remove_time_slot(), conv_to_min(),
    is_valid(), load_time_slots(), save_time_slots(), sort_time_slots()
    """

    def __init__(self, name=""):
        """Create DayCalendar object, setting self.name and self.time_slots."""
        self.name = name
        self.time_slots = []

    def __str__(self):
        """
        Define rules for printing day calendars.
        :return: string of name + all time slots
        """
        class_string = f"{self.name}'s Calender ({len(self.time_slots)} time slots):"
        for time_slot in self.time_slots:
            class_string += f"\n{time_slot}"
        return class_string

    def add_time_slot(self, time_slot=TimeSlot()):
        """Append time slot to time_slots list."""
        self.time_slots.append(time_slot)

    def remove_time_slot(self, time_slot=TimeSlot()):
        """Remove time slot from time_slots list."""
        if time_slot in self.time_slots:
            self.time_slots.remove(time_slot)

    def conv_to_min(self):
        """
        Return time slots list with times converted to total minutes from military time strings.
        :return: list of converted time slots
        """
        converted_time_slots = [time_slot.conv_to_min() for time_slot in self.time_slots.copy()]
        return converted_time_slots

    def load_time_slots(self, filename):
        """Read time slots from file and add them to time_slots list."""
        with open(filename, 'r') as file_in:
            for line in file_in:
                try:
                    start_time, end_time = [Time(part) for part in line.strip().split(",")]
                    self.time_slots.append(TimeSlot(start_time, end_time))
                except ValueError:
                    continue
                except IndexError:
                    continue

    def save_time_slots(self, filename):
        """Write time slots in list to a file."""
        with open(filename, 'w') as file_out:
            file_out.writelines((f"{time_slot.start_time.time},{time_slot.end_time.time}\n" for time_slot in self.time_slots))


if __name__ == '__main__':
    calendar1 = DayCalendar("Caleb Webster")
    calendar1.time_slots = [TimeSlot(Time("9:00"), Time("10:00")), TimeSlot(Time("13:00"), Time("14:30")), TimeSlot(Time("16:20"), Time("17:00"))]
    # calendar1.load_time_slots("my_calendar.csv")
    print(repr(calendar1.time_slots))
    time_slot_to_add = TimeSlot(Time("13:30"), Time("14:00"))
    calendar1.add_time_slot(time_slot_to_add)
    calendar1.remove_time_slot(time_slot_to_add)
    print(calendar1)
    print(calendar1.conv_to_min())
    calendar1.save_time_slots("my_calendar.csv")
