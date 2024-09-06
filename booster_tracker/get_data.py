import django
import os
import sys

sys.path.append("")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")
django.setup()

from booster_tracker.models import Launch, StageAndRecovery, SpacecraftOnLaunch

from django.db import transaction
from dateutil import parser
from datetime import datetime
from itertools import islice
from enum import StrEnum
import pytz

import csv
import statistics

sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")
django.setup()

import requests
from datetime import datetime

# API endpoint
url = "https://nextspaceflight.com/api/launches/"
url2 = "https://api.boostertracker.com/api/launchesonly/"

# Fetch data from the API
response = requests.get(url)
nxsf_data = response.json()["list"]

response = requests.get(url2)
my_data = response.json()


def parse_time(time_str):
    try:
        # Try to parse the time with microseconds
        return pytz.utc.localize(datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S.%fZ"))
    except ValueError:
        # Fallback to parsing without microseconds
        return pytz.utc.localize(datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ"))


# Filter launches where 'l' is 1 (SpaceX)
filtered_nxsf_launches = [launch for launch in nxsf_data if launch.get("l") == 1]
filtered_launches_2 = []
for launch in filtered_nxsf_launches:
    launch_name = launch.get("n")
    launch_id = launch.get("i")

    if launch_id != 5 and "Test Flight" in launch_name:
        continue
    else:
        filtered_launches_2.append(launch)

# Sort the launches by time
sorted_launches = sorted(filtered_launches_2, key=lambda x: parse_time(x["t"]))
print("BREAK")
# Print the sorted launches
for index, launch in enumerate(Launch.objects.all().order_by("time")):
    if launch.time > datetime(2024, 6, 2, 0, 0, tzinfo=pytz.utc):
        continue
    nxsf_launch_time = parse_time(sorted_launches[index]["t"])
    db_launch_time = launch.time

    nxsf_launch = sorted_launches[index]

    if nxsf_launch_time.date() != db_launch_time.date():
        print(launch["name"], "Date different")

    if nxsf_launch_time.hour != db_launch_time.hour:
        print(launch["name"], "Hour different")

    if nxsf_launch_time.hour != db_launch_time.hour:
        print(launch["name"], "Minute different")
