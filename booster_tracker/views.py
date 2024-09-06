from django.shortcuts import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
import requests
from datetime import datetime
import pytz
from booster_tracker.models import Launch


def health(request):
    return HttpResponse("Success", status=200)


@staff_member_required
def compare_launch_times(request):
    # API endpoints
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

    differences = []

    # Compare the launches
    for index, launch in enumerate(Launch.objects.all().order_by("time")):
        nxsf_launch_time = parse_time(sorted_launches[index]["t"])
        db_launch_time = launch.time

        if (
            nxsf_launch_time.date() != db_launch_time.date()
            or nxsf_launch_time.hour != db_launch_time.hour
            or nxsf_launch_time.minute != db_launch_time.minute
        ):
            continue
        else:
            launch.time = nxsf_launch_time
            launch.save(update_fields=["time"])

    return HttpResponse("Ran")
