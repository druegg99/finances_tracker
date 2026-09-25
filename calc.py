import datetime as dt

from entry import *


class Budget:
    def __init__(self, income: float = 0.0, expense: float = 0.0):
        self.income = income
        self.expense = expense

    def add_income(self, amount):
        self.income += amount

    def add_expense(self, amount):
        self.expense += amount

    def get_total(self) -> float:
        return self.income - self.expense

def add_entry_tentative(entry_list: list[Entry], amount: float, type: entry_type, label: str):
    entry = Entry(type, label, amount)
    entry_list.append(entry)

def remove_tentative_entry(entry_list: list[Entry], index: int):
    entry_list.pop(index)

def calculate_current_month(entry_tuple: tuple[list[RecurringEntry], list[RegularEntry], list[Entry]]) -> float:
    budget = Budget()
    today = dt.date.today()
    for entry in entry_tuple[1]:
        if entry.entry_time.month == today.month:
            if entry.entry == entry_type.IN:
                budget.add_income(entry.amount)
            if entry.entry == entry_type.OUT:
                budget.add_expense(entry.amount)
    for entry in entry_tuple[0]:
        pass #I need to review how to calculate time differences for recurring payments
    return budget.get_total()
