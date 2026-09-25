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

def calculate_current_month(entry_tuple: tuple[list[RecurringEntry], list[RegularEntry], list[Entry]]) -> Budget:
    budget = Budget()
    today = dt.date.today()
    for entry in entry_tuple[1]:
        if entry.entry_time.month == today.month:
            if entry.entry == entry_type.IN:
                budget.add_income(entry.amount)
            if entry.entry == entry_type.OUT:
                budget.add_expense(entry.amount)
    for entry in entry_tuple[0]:
        if entry.end_date == None or entry.end_date > dt.date(today.year, today.month, 1):
            if entry.frequency == recurring_type.YEARLY and entry.start_date.month == today.month:
                if entry.entry == entry_type.IN:
                    budget.add_income(entry.amount)
                if entry.entry == entry_type.OUT:
                    budget.add_expense(entry.amount)
            if entry.frequency == recurring_type.MONTHLY and entry.start_date.day <= today.day:
                if entry.entry == entry_type.IN:
                    budget.add_income(entry.amount)
                if entry.entry == entry_type.OUT:
                    budget.add_expense(entry.amount)
            if entry.frequency == recurring_type.DAILY:
                if entry.end_date == None or entry.end_date >= today:
                    if entry.entry == entry_type.IN:
                        budget.add_income(entry.amount * today.day)
                    if entry.entry == entry_type.OUT:
                        budget.add_expense(entry.amount * today.day)
                if entry.end_date != None and entry.end_date < today:
                    if entry.entry == entry_type.IN:
                        budget.add_income(entry.amount * entry.end_date.day)
                    if entry.entry == entry_type.OUT:
                        budget.add_expense(entry.amount * entry.end_date.day)
            if entry.frequency == recurring_type.CUSTOM:
                if entry.end_date == None or entry.end_date >= dt.date(today.year, today.month, 1):
                    months_last_charge = today
                    if entry.end_date <= today:
                        months_last_charge = entry.end_date
                    day_before_month = dt.date(today.year, today.month, 1) - dt.timedelta(days = 1)
                    charged_days = day_before_month - entry.start_date
                    last_charge = day_before_month - dt.timedelta(days = charged_days.days % entry.custom_frequency)
                    first_charge = last_charge + dt.timedelta(days = entry.custom_frequency)
                    charges_this_month = (months_last_charge - first_charge).days // entry.custom_frequency
                    if entry.entry == entry_type.IN:
                        budget.add_income(entry.amount * charges_this_month)
                    if entry.entry == entry_type.OUT:
                        budget.add_expense(entry.amount * charges_this_month)

    return budget
