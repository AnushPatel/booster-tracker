from enum import StrEnum
import re

# This section we create StrEnums to limit options in functions. While not used in this document, these are often used in models.py


class TurnaroundObjects(StrEnum):
    BOOSTER = "booster"
    SECOND_STAGE = "second stage"
    LANDING_ZONE = "landing zone"
    PAD = "pad"
    ALL = "all"
    SPACECRAFT = "spacecraft"


# First several functions will be defined that are commonly used.
# As the name implies, this formats the time to be in the following format: March 25, 2024 04:38 UTC


def format_time(time_obj):
    formatted_date = time_obj.strftime("%B %d, %Y")
    formatted_time = time_obj.strftime("%H:%M")
    timezone_abbr = time_obj.strftime("%Z")

    formatted_str = f"{formatted_date} - {formatted_time} {timezone_abbr}"

    return formatted_str


# This converts from seconds to a human readable format in days, hours, minutes, and seconds. If any are zero, they are removed.


def convert_seconds(x):
    d = int(x / 86400)
    x -= d * 86400
    h = int(x / 3600)
    x -= h * 3600
    m = int(x / 60)
    x -= m * 60
    s = round(x)

    time_units = []
    if d:
        time_units.append(f"{d} day{'s' if d != 1 else ''}")
    if h:
        time_units.append(f"{h} hour{'s' if h != 1 else ''}")
    if m:
        time_units.append(f"{m} minute{'s' if m != 1 else ''}")
    if s:
        time_units.append(f"{s} second{'s' if s != 1 else ''}")

    if len(time_units) > 2:
        time_str = ", ".join(time_units[:-1]) + ", and " + time_units[-1]
    elif len(time_units) == 2:
        time_str = time_units[0] + " and " + time_units[1]
    elif len(time_units) == 1:
        time_str = time_units[0]
    else:
        time_str = "0 seconds"

    return time_str


# Makes an ordinal; 1 -> 1st


def make_ordinal(n: int):
    if n is None:
        return "None"
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix


# Takes in a list of items and returns them in concatinated form [Bob, Doug, GO Beyond] -> Bob, Doug, and GO Beyond
def concatenated_list(items):
    return (
        items[0]
        if len(items) == 1
        else (", ".join(items[:-1]) + (", and " if len(items) > 2 else " and ") + str(items[-1]) if items else "N/A")
    )


def success(value: str) -> str:
    """Converts landings to be human readable and gramatically correct"""
    if value == "SUCCESS" or value is None:
        return "successfully completed"
    if value == "PRECLUDED":
        return "was precluded from completing"
    return "failed to complete"


def turnaround_time(launches: list) -> int:
    """Returns turnaround between last two launches in list; in total seconds"""
    if len(launches) > 1:
        return (launches[len(launches) - 1].time - launches[len(launches) - 2].time).total_seconds()
    return None


def all_values_true(dictionary):
    """Returns if all values in a tree are true"""
    if isinstance(dictionary, bool):
        return dictionary
    if isinstance(dictionary, dict):
        return all(all_values_true(value) for value in dictionary.values())
    return False


def version_format(string):
    """Returns custom formatting for versions (V1.0 -> v1.0)"""
    regex = r"^V\d"
    if re.match(regex, string):
        return "v" + string[1:]
    return string


def get_averages(values, chunk_size):
    averages = []
    for i in range(0, len(values), chunk_size):
        chunk = values[i : i + chunk_size]
        avg = sum(chunk) / len(chunk) if chunk else 0
        averages.append(avg)
    return averages
