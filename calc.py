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

def calculate_range(entry_tuple: tuple[list[RecurringEntry], list[RegularEntry], list[Entry]], start: dt.date, end: dt.date) -> Budget:

    if end > start:
        raise ValueError(DATE_RANGE_INCORRECT)
    budget = Budget()
    # check one time entries first, easier
    for entry in entry_tuple[1]:
        if entry.entry_time >= start and entry.entry_time <= end:
            if entry.entry == entry_type.IN:
                budget.add_income(entry.amount)
            if entry.entry == entry_type.OUT:
                budget.add_expense(entry.amount)
    #the pain begins
    for entry in entry_tuple[0]:
        if entry.end_date == None or entry.end_date >= start:
            if entry.end_date != None and entry.end_date <= end:
                instance_end = entry.end_date
            else:
                instance_end = end

            if entry.start_date > start:
                instance_start = entry.start_date
            else:
                instance_start = start

            match entry.frequency:
                case recurring_type.YEARLY:
                    instance_month = entry.start_date.month
                    instance_day = entry.start_date.day
                    last_year_inclusive = False
                    first_year_inclusive = False
                    if instance_start.month <= instance_month:
                        if instance_start.day <= instance_day:
                            first_year_inclusive = True
                    if instance_end.month >= instance_month:
                        if instance_end.day >= instance_day:
                            last_year_inclusive = True
                    if entry.entry == entry_type.IN:
                        budget.add_income(entry.amount * ((instance_end.year - instance_start.year) - 1 + last_year_inclusive + first_year_inclusive))
                    if entry.entry == entry_type.OUT:
                        budget.add_expense(entry.amount * ((instance_end.year - instance_start.year) - 1 + last_year_inclusive + first_year_inclusive))
                case recurring_type.MONTHLY:
                    instance_day = entry.start_date.day
                    first_month_inclusive = False
                    last_month_inclusive = False
                    #cursed different length months
                    if instance_start.month == entry.start_date.month:
                        if instance_start.day <= instance_day:
                            first_month_inclusive = True
                    if instance_start.day <= instance_day:
                        first_month_inclusive = True
                    #truncated for end month simplicity
                    if instance_day > 28:
                        instance_day = 28
                    if instance_end.day <= instance_day:
                        last_month_inclusive = True
                    head_months = 12 - instance_start.month + first_month_inclusive
                    tail_months = instance_end.month - 1 + last_month_inclusive
                    middle_months = (instance_end.year - instance_start.year - 1) * 12
                    if entry.entry == entry_type.IN:
                        budget.add_income(entry.amount * (head_months + tail_months + middle_months))
                    if entry.entry == entry_type.OUT:
                        budget.add_expense(entry.amount * (head_months + tail_months + middle_months))
                case recurring_type.DAILY:
                    delta = instance_end - instance_start
                    if entry.entry == entry_type.IN:
                        budget.add_income(entry.amount * (delta.days + 1))
                    if entry.entry == entry_type.OUT:
                        budget.add_expense(entry.amount * (delta.days + 1))
                case recurring_type.CUSTOM:
                    delta_start = instance_start - entry.start_date
                    days_later = delta_start.days % entry.custom_frequency.days
                    if days_later > 0:
                        instance_start = instance_start + entry.custom_frequency - dt.timedelta(days=days_later)
                    total_delta = instance_end - instance_start
                    if entry.entry == entry_type.IN:
                        budget.add_income(entry.amount * (total_delta.days // entry.custom_frequency.days))
                    if entry.entry == entry_type.OUT:
                        budget.add_expense(entry.amount * (total_delta.days // entry.custom_frequency.days))
        #else: not necessary, just ignore out of range entries from loop

    return budget

def calculate_current_month(entry_tuple: tuple[list[RecurringEntry], list[RegularEntry], list[Entry]]) -> Budget:
    today = dt.date.today()
    return calculate_range(entry_tuple, dt.date(today.year, today.month, 1), today)

def calculate_current_year(entry_tuple: tuple[list[RecurringEntry], list[RegularEntry], list[Entry]]) -> Budget:
    today = dt.date.today()
    return calculate_range(entry_tuple, dt.date(today.year, 1, 1), today)

#    budget = Budget()
#    today = dt.date.today()
#    for entry in entry_tuple[1]:
#        if entry.entry_time.month == today.month:
#            if entry.entry == entry_type.IN:
#                budget.add_income(entry.amount)
#            if entry.entry == entry_type.OUT:
#                budget.add_expense(entry.amount)
#    for entry in entry_tuple[0]:
#        if entry.end_date == None or entry.end_date > dt.date(today.year, today.month, 1):
#            if entry.frequency == recurring_type.YEARLY and entry.start_date.month == today.month:
#                if entry.entry == entry_type.IN:
#                    budget.add_income(entry.amount)
#                if entry.entry == entry_type.OUT:
#                    budget.add_expense(entry.amount)
#            if entry.frequency == recurring_type.MONTHLY and entry.start_date.day <= today.day:
#                if entry.entry == entry_type.IN:
#                    budget.add_income(entry.amount)
#                if entry.entry == entry_type.OUT:
#                    budget.add_expense(entry.amount)
#            if entry.frequency == recurring_type.DAILY:
#                if entry.end_date == None or entry.end_date >= today:
#                    if entry.entry == entry_type.IN:
#                        budget.add_income(entry.amount * today.day)
#                    if entry.entry == entry_type.OUT:
#                        budget.add_expense(entry.amount * today.day)
#                if entry.end_date != None and entry.end_date < today:
#                    if entry.entry == entry_type.IN:
#                        budget.add_income(entry.amount * entry.end_date.day)
#                    if entry.entry == entry_type.OUT:
#                        budget.add_expense(entry.amount * entry.end_date.day)
#            if entry.frequency == recurring_type.CUSTOM:
#                if entry.end_date == None or entry.end_date >= dt.date(today.year, today.month, 1):
#                    months_last_charge = today
#                    if entry.end_date <= today:
#                        months_last_charge = entry.end_date
#                    day_before_month = dt.date(today.year, today.month, 1) - dt.timedelta(days = 1)
#                    charged_days = day_before_month - entry.start_date
#                    last_charge = day_before_month - dt.timedelta(days = charged_days.days % entry.custom_frequency)
#                    first_charge = last_charge + dt.timedelta(days = entry.custom_frequency)
#                    charges_this_month = (months_last_charge - first_charge).days // entry.custom_frequency
#                    if entry.entry == entry_type.IN:
#                        budget.add_income(entry.amount * charges_this_month)
#                    if entry.entry == entry_type.OUT:
#                        budget.add_expense(entry.amount * charges_this_month)
#
#    return budget
