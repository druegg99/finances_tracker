import os
import shutil
from entry.py import *
from configvars import *

#finances.dat format:
# RECURRING
# entries...
#
# REGULAR
# entries,..
#
# tentative entries (parent Entry class) aren't saved.
# recurring entry format: IN/OUT, <quantity float>, recurring_type, <freq int days>, start_date year, start_date month, start_date day, end_date year, end_date month, end_date day, label
# regular entry format: IN/OUT, <quantity float>, date year, date month, date day, label


def str_to_recurring(input: str) -> RecurringEntry:
    elements = input.split(", ", 10) #limit splits to 10, in case label contains commas

    type: entry_type = None
    if elements[0] == "income":
        type = IN
    if elements[0] == "expense":
        type = OUT
    if type == None:
        raise ValueError(DAT_INCORRECT)
    #If we get this far, database is likely correct so no more checks out of laziness

    amount = float(elements[1])

    frequency_type: recurring_type = None
    if elements[2] == "yearly":
        frequency_type = YEARLY
    if elements[2] == "monthly":
        frequency_type = MONTHLY
    if elements[2] == "daily":
        frequency_type = DAILY
    if elements[2] == "custom":
        frequency_type = CUSTOM

    frequency_days: int = int(elements[3])

    start_year = int(elements[4])
    start_month = int(elements[5])
    start_day = int(elements[6])
    end_year = int(elements[7])
    end_month = int(elements[8])
    end_day = int(elements[9])

    label = elements[10]

    entry = RecurringEntry(type, label, amount, frequency_type, frequency_days)
    entry.set_start(start_year, start_month, start_day)
    if end_year > 0: #if end_date is None, format will write 0, 0, 0 for end date
        entry.set_end(end_year, end_month, end_day)

    return entry

def str_to_regular(input: str) -> RegularEntry:
    elements = input.split(", ", 5)

    type: entry_type = None
    if elements[0] == "income":
        type = IN
    if elements[0] == "expense":
        type = OUT
    if type == None:
        raise ValueError(DAT_INCORRECT)

    amount = float(elements[1])

    year = int(elements[2])
    month = int(elements[3])
    day = int(elements[4])

    label = elements[5]

    entry = RegularEntry(type, label, amount)
    entry.set_date(year, month, day)

    return entry

def recurring_to_str(input: RecurringEntry) -> str:
    if input.end_date == None:
        return f"{input.entry}, {input.amount}, {input.frequency}, {input.custom_frequency.days}, {input.start_date.year}, {input.start_date.month}, {input.start_date.day}, 0, 0, 0, {input.label}"
    else:
        return f"{input.entry}, {input.amount}, {input.frequency}, {input.custom_frequency.days}, {input.start_date.year}, {input.start_date.month}, {input.start_date.day}, {input.end_date.year}, {input.end_date.month}, {input.end_date.day}, {input.label}"

def regular_to_str(input: RegularEntry) -> str:
    return f"{input.entry}, {input.amount}, {input.date.year}, {input.date.month}, {input.date.day}, {input.label}"


def load_database(path: str = DAT_PATH) -> (list[RecurringEntry], list[RegularEntry]):
    if not os.path.exists(path):
        raise OSError(-1, DAT_NOTFOUND)
    else:
        with open(path, "r") as f:
            database = r.read()
        dat_sections = database.split("\n\n")
        if dat_sections[0][:9] != "RECURRING" or dat_sections[1][:7] != "REGULAR":
            raise ValueError(DAT_INCORRECT)
        else:
            recurring_entries: list[Entry] = []
            regular_entries: list[Entry] = []
            recurring = dat_sections[0].split("\n")[1:]
            regular = dat_sections[1].split("\n")[1:-1] #write_database adds an extra line break in the end, hence the last line is removed
            if recurring[0] != "None":
                for item in recurring:
                    recurring_entries.append(str_to_recurring(item))
            if regular[0] != "None":
                for item in regular:
                    regular_entries.append(str_to_regular(item))
            return (recurring_entries, regular_entries)

def write_database(path: str = DAT_PATH, regular_entries: list[RegularEntry], recurring_entries: list[RecurringEntry]) -> None:
    if not os.path.exists(os.path.dirname(path)):
        os.mkdirs(os.path.dirname(path))
    while open(path, "x") as f:
        f.write("RECURRING\n")
        if recurring_entries:
            for item in recurring_entries:
                f.write(recurring_to_str(item) + "\n")
        else:
            f.write("None\n")
        f.write("\nREGULAR\n")
        if recurring_entries:
            for item in regular_entries:
                f.write(regular_to_str(item) + "\n")
        else:
            f.write("None\n")
