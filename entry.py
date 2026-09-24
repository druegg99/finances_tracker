import datetime
from enum import Enum

class entry_type(Enum):
    IN = "income"
    OUT = "expense"

class entry():
    def __init__(self, entry: entry_type, amount: float):
        self.entry_time = datetime.datetime.now()
        self.entry = entry
        self.amount = amount

class recurring_entry():
    def __init__(self, entry: entry_type, amount: float):
        self.entry = entry
        self.amount = amount
        self.start_date = datetime.datetime.now()
        self.end_date = None

    def end_now(self):
        self.end_date = datetime.datetime.now()

    def set_end(self, year: int, month: int, day: int):
        try:
            self.end_date = datetime.datetime(year, month, day)
        except:
            print("Incorrect date format.")
