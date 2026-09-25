import datetime as dt
from enum import Enum

class entry_type(Enum):
    IN = "income"
    OUT = "expense"
    def __str__(self):
        return self.value #should make formatting easier

class recurring_type(Enum):
    YEARLY = "yearly"
    MONTHLY = "monthly"
    DAILY = "daily"
    CUSTOM = "custom"
    def __str__(self):
        return self.value #should make formatting easier

class Entry():
    def __init__(self, entry: entry_type, label: str, amount: float):
        self.entry = entry
        self.amount = amount
        self.label = label

class RegularEntry(Entry):
    def __init__(self, entry: entry_type, label: str, amount: float):
        super().__init__(entry, label, amount)
        self.entry_time = dt.date.today()

    def set_date(self, year: int, month: int, day: int):
        try:
            self.start_date = dt.date(year, month, day)
        except:
            print("Incorrect date format.")

class RecurringEntry(Entry):
    def __init__(self, entry: entry_type, label: str, amount: float, frequency: recurring_type, frequency_days: int = 0):
        super().__init__(entry, label, amount)
        self.start_date = dt.date.today()
        self.end_date = None
        self.frequency = frequency
        self.custom_frequency = dt.timedelta(days = frequency_days)

    def end_now(self):
        self.end_date = dt.date.today()

    def set_end(self, year: int, month: int, day: int):
        try:
            self.end_date = dt.date(year, month, day)
        except:
            print("Incorrect date format.")

    def set_start(self, year: int, month: int, day: int):
        try:
            self.start_date = dt.date(year, month, day)
        except:
            print("Incorrect date format.")

#    def set_frequency(frequency: recurring_type, frequency_days: int):
#        if recurring_type is CUSTOM:
#            return --- unfinished, not necessary
