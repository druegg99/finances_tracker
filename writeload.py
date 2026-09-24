import os
import shutil
from entry.py import *

#finances.dat format:
# RECURRING
# entries...
#
# REGULAR
# entries,..
#
# tentative entries (parent Entry class) aren't saved.

DAT_PATH = "databse/finances.dat"
DAT_NOTFOUND = "Database not found"
DAT_INCORRECT = "Database formatted incorrectly"

def str_to_recurring(input: str) -> RecurringEntry:
    pass

def str_to_regular(input: str) -> RegularEntry:
    pass

def recurring_to_str(input: RecurringEntry) -> str:
    pass

def regular_to_str(input: RegularEntry) -> str:
    pass


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
