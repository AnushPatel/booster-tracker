from enum import StrEnum
from collections import defaultdict
import re
from datetime import datetime
import pytz

# This section we create StrEnums to limit options in functions. While not used in this document, these are often used in models.py


class TurnaroundObjects(StrEnum):
    BOOSTER = "booster"
    SECOND_STAGE = "second stage"
    LANDING_ZONE = "landing zone"
    PAD = "pad"
    ALL = "all"
    SPACECRAFT = "spacecraft"


class MonotonicDirections(StrEnum):
    INCREASING = "increasing"
    DECREASING = "decreasing"


# First several functions will be defined that are commonly used.
def format_time(time_obj: datetime) -> str:
    """formats the time to be in the following format: March 25, 2024 04:38 UTC"""
    formatted_date = time_obj.strftime("%B %d, %Y")
    formatted_time = time_obj.strftime("%H:%M")
    timezone_abbr = time_obj.strftime("%Z")

    formatted_str = f"{formatted_date} - {formatted_time} {timezone_abbr}"

    return formatted_str


def convert_seconds(x) -> str:
    """Converts from seconds to a human readable format in days, hours, minutes, and seconds. If any are zero, they are removed."""
    if x is None:
        return None
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
def make_ordinal(n: int) -> str:
    """Returns the ordinal of an int"""
    if n is None:
        return "None"
    if 11 <= (n % 100) <= 13:
        suffix = "th"
    else:
        suffix = ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix


def concatenated_list(items) -> str:
    """Takes in a list of items and returns a string in concatenated form; [Bob, Doug, GO Beyond] -> Bob, Doug, and GO Beyond"""
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


def version_format(string) -> str:
    """Returns custom formatting for versions (V1.0 -> v1.0)"""
    regex = r"^V\d"
    if re.match(regex, string):
        return "v" + string[1:]
    return string


def get_averages(values: list, chunk_size: int, round_to_place: int) -> list:
    """For a given list, averages chunks of chunk_size, creating a smaller object"""
    averages = []
    for i in range(0, len(values), chunk_size):
        chunk = values[i : i + chunk_size]
        avg = round(sum(chunk) / len(chunk), round_to_place) if chunk else 0
        averages.append(avg)
    return averages


def make_monotonic(list: list, order: MonotonicDirections) -> list:
    """Takes in a list and makes it monotonic"""
    for index, value in enumerate(list):
        if order == MonotonicDirections.INCREASING:
            if index == 0:
                continue
            if value < list[index - 1]:
                list[index] = list[index - 1]
        if order == MonotonicDirections.DECREASING:
            if index == len(list) - 1:
                continue
            if value < list[index + 1]:
                list[index] = list[index + 1]

    return list


def all_zeros(list: list) -> bool:
    """Returns if all values in a list are 0"""
    return all(v == 0 for v in list)


def combine_dicts(dict1: dict, dict2: dict) -> dict:
    """For dicts with arrays as values, combines the arrays for equal keys; returns dict with combined arrays"""
    combined = defaultdict(list)

    for key, value in dict1.items():
        combined[key].extend(value)

    if dict2:
        for key, value in dict2.items():
            combined[key].extend(value)

    for key in combined:
        combined[key] = list(set(combined[key]))

    return dict(combined)


def parse_start_time(query_params, default_start_date: datetime) -> datetime:
    """Checks to see if query specifies start date; else returns default_start_date"""
    date_str: str = query_params.get("startdate", "")
    if date_str:
        return datetime.strptime(date_str.strip('"').replace("Z", ""), "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=pytz.utc)
    return default_start_date


def is_significant(nums) -> bool:
    significant_nums = {1, 10, 25, 50}

    if isinstance(nums, list):
        return any(num % 100 == 0 or num in significant_nums for num in nums)
    elif isinstance(nums, int):
        return nums % 100 == 0 or nums in significant_nums

    return False


def get_start_date(last_object):
    if last_object:
        if hasattr(last_object, "launch") and (time := last_object.launch.time):
            return time
        if hasattr(last_object, "time") and (time := last_object.time):
            return time
    return datetime.now(pytz.utc)


def build_table_html(data):
    table_html = "<table>"
    for key, values in data.items():
        table_html += f'<tr><th class="has-text-align-left" data-align="left"><h6><strong>{key}</strong></h6></th>'
        table_html += "<td>"
        for value in values:
            table_html += f"<em>{value}</em><br>"
        table_html += "</td></tr>"
    table_html += "</table>"
    return table_html
