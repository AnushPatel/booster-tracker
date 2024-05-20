from __future__ import annotations
import pytz
from booster_tracker.models import *
from datetime import datetime
from enum import StrEnum
from django.db.models import Q, Count, Max

#First several functions will be defined that are commonly used. 
#As the name implies, this formats the time to be in the following format: March 25, 2024 04:38 UTC
def format_time(time_obj):
    formatted_date = time_obj.strftime("%B %d, %Y")
    formatted_time = time_obj.strftime("%H:%M")
    timezone_abbr = time_obj.strftime("%Z")
    
    formatted_str = f"{formatted_date} - {formatted_time} {timezone_abbr}"

    return formatted_str

#This converts from seconds to a human readable format in days, hours, minutes, and seconds. If any are zero, they are removed.
def convert_seconds(x):
    d = int(x/86400)
    x -= (d*86400)
    h = int(x/3600)
    x -= (h*3600)
    m = int(x/60)
    x -= (m*60)
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
        time_str = ', '.join(time_units[:-1]) + ', and ' + time_units[-1]
    elif len(time_units) == 2:
        time_str = time_units[0] + ' and ' + time_units[1]
    elif len(time_units) == 1:
        time_str = time_units[0]
    else:
        time_str = "0 seconds"

    return time_str

#Makes an ordinal; 1 -> 1st
def make_ordinal(n: int):
    if n is None:
        return "None"
    elif 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

#Takes in a list of items and returns them in concatinated form [Bob, Doug, GO Beyond] -> Bob, Doug, and GO Beyond
concatenated_list = lambda items: items[0] if len(items) == 1 else ', '.join(items[:-1]) + (', and ' if len(items) > 2 else ' and ') + str(items[-1]) if items else 'N/A'

def get_most_flown_boosters():
    booster_and_launch_count = Stage.objects.filter(stageandrecovery__launch__time__lte=datetime.now(pytz.utc), type="BOOSTER", rocket__name__icontains="Falcon").annotate(launch_count=Count('stageandrecovery__launch', distinct=True))
    max_launch_count = booster_and_launch_count.aggregate(Max('launch_count'))['launch_count__max']
    most_flown_boosters = list(booster_and_launch_count.filter(launch_count=max_launch_count).values_list("name", flat=True))

    return(most_flown_boosters, max_launch_count)

#This item creates a list without any repeats
def remove_duplicates(objects: list[Boat]) -> list:
    names: set[str] = set()
    for item in objects:
        names.add(item.name)
    return list(names)

#Helps convert boolean to human readable text in stats
def success(value: str) -> str:
    if value == "SUCCESS" or value is None:
        return "successfully completed"
    elif value == "PRECLUDED":
        return "was precluded from completing"
    return "failed to complete"

#This section we create StrEnums to limit options in functions
class TurnaroundObjects(StrEnum):
    BOOSTER = "booster"
    SECOND_STAGE = "second stage"
    LANDING_ZONE = "landing zone"
    PAD = "pad"
    ALL = "all"

#Simply gets the turnaround time between two objects; the exact list should be specified elsewhere
def turnaround_time(launches: list[Launch]) -> int:
    if len(launches) > 1:
        return((launches[len(launches)-1].time-launches[len(launches)-2].time).total_seconds())
    return None

#This section we'll define functions that are used for generating the home page:
def get_launches_and_successes_per_rocket() -> list:
    values: list = []
    for rocket in Rocket.objects.all():
        launches = Launch.objects.filter(rocket=rocket, time__lte=datetime.now(pytz.utc)).count()
        successes = Launch.objects.filter(rocket=rocket, launch_outcome="SUCCESS", time__lte=datetime.now(pytz.utc)).count()
        values.append([rocket.name, launches, successes])

    return values

def get_landings_and_successes() -> tuple:
    num_landing_attempts = StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc)).filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).filter(~Q(method_success="PRECLUDED")).count()
    num_successes = StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc), method_success="SUCCESS").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).count()

    return (num_landing_attempts, num_successes)