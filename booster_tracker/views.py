from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
from django.db.models import Q
from django.templatetags.static import static
from booster_tracker.utils import TurnaroundObjects
from booster_tracker.home_utils import (
    get_next_and_last_launches,
    gather_launch_info,
    gather_stats,
    get_last_starship_launch,
    gather_launch_stats,
    gather_landing_stats,
    gather_most_flown_stages,
    get_quickest_turnaround,
    gather_reflights_stats,
    get_starship_reflights,
    gather_recovery_zone_stats,
    gather_pad_stats,
)

import pytz
import statistics
from datetime import datetime

from booster_tracker.models import (
    Stage,
    StageAndRecovery,
    Launch,
    Spacecraft,
    SpacecraftOnLaunch,
    RocketFamily,
)


def launches_list(request):
    # Get the search query from the request
    query = request.GET.get("q")

    # Fetch all launches, optionally filtering by search query
    if query:
        launches = Launch.objects.filter(name__icontains=query).order_by("-time")
    else:
        launches = Launch.objects.all().order_by("-time")

    # Number of launches per page
    per_page = 50

    # Create a paginator object
    paginator = Paginator(launches, per_page)

    # Get the current page number from the request
    page_number = request.GET.get("page", 1)

    try:
        # Get the launches for the current page
        paginated_launches = paginator.page(page_number)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        paginated_launches = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page of results
        paginated_launches = paginator.page(paginator.num_pages)

    context = {
        "paginated_launches": paginated_launches,
        "query": query,
    }

    return render(request, "launches/launches_list.html", context)


def home(request):
    cache_key = "home_page"
    cached_content = cache.get(cache_key)

    if cached_content:
        return cached_content

    next_launch, last_launch = get_next_and_last_launches()

    if not last_launch:
        context = {
            "next_launch": next_launch,
            "last_launch": None,
            "next_launch_boosters": "Unknown",
            "next_launch_recoveries": "",
            "next_launch_tugs": "",
            "next_launch_fairing_recovery": "",
            "next_launch_photo": static("images/falcon_9.jpg"),
            "last_launch_boosters": None,
            "last_launch_recoveries": None,
            "last_launch_tugs": None,
            "last_launch_fairing_recovery": None,
            "most_flown_boosters": "N/A",
            "quickest_booster_turnaround": "N/A",
            "falcon_heavy_reflights": "N/A",
            "falcon_9_reflights": "N/A",
            "pad_stats": [],
            "zone_stats": [],
            "shortest_time_between_launches": "N/A",
        }
        return render(request, "launches/home.html", context)

    if next_launch:
        (
            next_launch_boosters,
            next_launch_recoveries,
            next_launch_tugs,
            next_launch_fairing_recovery,
            next_launch_photo,
        ) = gather_launch_info(next_launch)
    else:
        next_launch_boosters = "Unknown"
        next_launch_recoveries = ""
        next_launch_tugs = ""
        next_launch_fairing_recovery = ""
        next_launch_photo = static("images/falcon_9.jpg")

    (
        last_launch_boosters,
        last_launch_recoveries,
        last_launch_tugs,
        last_launch_fairing_recovery,
        _,
    ) = gather_launch_info(last_launch)

    stats = gather_stats(last_launch)
    pad_stats = gather_pad_stats(rocket_name="Falcon")
    recovery_zone_stats = gather_recovery_zone_stats(rocket_name="Falcon")

    context = {
        "launches_per_vehicle": stats["num_launches_per_rocket_and_successes"],
        "num_landings": stats["num_landings_and_successes"],
        "num_booster_reflights": stats["num_booster_reflights"],
        "next_launch": next_launch,
        "last_launch": last_launch,
        "next_launch_boosters": next_launch_boosters,
        "next_launch_recoveries": next_launch_recoveries,
        "next_launch_tugs": next_launch_tugs,
        "next_launch_fairing_recovery": next_launch_fairing_recovery,
        "next_launch_photo": next_launch_photo,
        "last_launch_boosters": last_launch_boosters,
        "last_launch_recoveries": last_launch_recoveries,
        "last_launch_tugs": last_launch_tugs,
        "last_launch_fairing_recovery": last_launch_fairing_recovery,
        "most_flown_boosters": stats["most_flown_boosters_string"],
        "quickest_booster_turnaround": stats["quickest_booster_turnaround_string"],
        "falcon_heavy_reflights": stats["falcon_heavy_reflights"],
        "falcon_9_reflights": stats["falcon_9_reflights"],
        "pad_stats": pad_stats,
        "zone_stats": recovery_zone_stats,
        "shortest_time_between_launches": stats["shortest_time_between_launches"],
    }

    rendered_content = render(request, "launches/home.html", context)
    cache.set(cache_key, rendered_content, timeout=None)

    return rendered_content


def launch_details(request, launch_name):
    launch = get_object_or_404(Launch, name=launch_name)
    context = {"data": launch.create_launch_table(), "launch": launch}
    return render(request, "launches/launch_table.html", context)


def stage_list(request, rocket_family: RocketFamily, stage_type):
    stages = Stage.objects.filter(rocket__family__name__icontains=rocket_family, type__icontains=stage_type)

    active_stages = stages.filter(status="ACTIVE").order_by("name")
    lost_stages = stages.filter(Q(status="LOST") | Q(status="EXPENDED")).order_by("name")
    retired_stages = stages.filter(status="RETIRED").order_by("name")

    context = {
        "active_stages": active_stages,
        "retired_stages": retired_stages,
        "lost_stages": lost_stages,
        "stage_type": stage_type,
        "rocket_family": rocket_family,
    }

    return render(request, "stages/stage_list.html", context)


def stage_info(request, rocket_family: RocketFamily, stage_type, stage_name):
    stage = get_object_or_404(
        Stage,
        name=stage_name,
        rocket__name__icontains=rocket_family,
        type__icontains=stage_type,
    )
    launches = Launch.objects.filter(stageandrecovery__stage=stage).order_by("time")
    launches_information = []
    turnarounds = []

    for launch in launches:
        turnaround = launch.get_stage_flights_and_turnaround(stage=stage)[1]
        launches_information.append(
            [
                launch,
                turnaround,
                StageAndRecovery.objects.get(launch=launch, stage=stage),
            ]
        )
        if turnaround and launch.time < datetime.now(pytz.utc):
            turnarounds.append(turnaround)

    average_turnaround = None
    turnaround_stdev = None
    quickest_turnaround = None

    if len(turnarounds) > 0:
        average_turnaround = round(statistics.mean(turnarounds), 2)
        quickest_turnaround = round(min(turnarounds), 2)
    if len(turnarounds) > 1:
        turnaround_stdev = round(statistics.stdev(turnarounds), 2)

    context = {
        "stage": stage,
        "launches": launches_information,
        "average_turnaround": average_turnaround,
        "stdev": turnaround_stdev,
        "quickest_turnaround": quickest_turnaround,
    }

    return render(request, "stages/stage_info.html", context)


def dragon_list(request):
    dragons = Spacecraft.objects.filter(family__name="Dragon")

    active_dragons = dragons.filter(status="ACTIVE").order_by("name")
    lost_dragons = dragons.filter(Q(status="LOST") | Q(status="EXPENDED")).order_by("name")
    retired_dragons = dragons.filter(status="RETIRED").order_by("name")

    context = {
        "active_dragons": active_dragons,
        "retired_dragons": retired_dragons,
        "lost_dragons": lost_dragons,
    }

    return render(request, "dragons/dragon_list.html", context)


def dragon_info(request, dragon_name):
    dragon = get_object_or_404(Spacecraft, name=dragon_name, family__name="Dragon")
    launches = Launch.objects.filter(spacecraftonlaunch__spacecraft=dragon).order_by("time")
    launches_information = []
    turnarounds = []

    for launch in launches:
        spacecraft_on_launch = SpacecraftOnLaunch.objects.get(launch=launch)
        turnaround = spacecraft_on_launch.get_spacecraft_turnaround()
        launches_information.append([launch, turnaround, spacecraft_on_launch])
        if turnaround and launch.time < datetime.now(pytz.utc):
            turnarounds.append(turnaround)

    average_turnaround = None
    turnaround_stdev = None
    quickest_turnaround = None

    if len(turnarounds) > 0:
        average_turnaround = round(statistics.mean(turnarounds), 2)
        quickest_turnaround = round(min(turnarounds), 2)
    if len(turnarounds) > 1:
        turnaround_stdev = round(statistics.stdev(turnarounds), 2)

    context = {
        "dragon": dragon,
        "launches": launches_information,
        "average_turnaround": average_turnaround,
        "stdev": turnaround_stdev,
        "quickest_turnaround": quickest_turnaround,
    }

    return render(request, "dragons/dragon_info.html", context)


def starship_home(request):
    rocket_name = "Starship"

    last_launch = get_last_starship_launch()
    num_launches_per_rocket_and_successes = gather_launch_stats(rocket_name)

    landing_stats = gather_landing_stats(rocket_name)
    most_flown_boosters_string, most_flown_ships_string = gather_most_flown_stages(rocket_name)

    quickest_booster_turnaround_string = get_quickest_turnaround(last_launch, TurnaroundObjects.BOOSTER)
    quickest_ship_turnaround_string = get_quickest_turnaround(last_launch, TurnaroundObjects.SECOND_STAGE)

    num_booster_reflights, num_ship_reflights = gather_reflights_stats(rocket_name)
    starship_reflights = get_starship_reflights()

    pad_stats = gather_pad_stats(rocket_name)
    recovery_zone_stats = gather_recovery_zone_stats(rocket_name)

    context = {
        "launches_per_vehicle": num_launches_per_rocket_and_successes,
        "booster_landing_attempts": landing_stats["booster_landing_attempts"],
        "ship_landing_attempts": landing_stats["ship_landing_attempts"],
        "booster_landing_successes": landing_stats["booster_landing_successes"],
        "ship_landing_successes": landing_stats["ship_landing_successes"],
        "most_flown_boosters": most_flown_boosters_string,
        "most_flown_ships": most_flown_ships_string,
        "quickest_booster_turnaround": quickest_booster_turnaround_string,
        "quickest_ship_turnaround": quickest_ship_turnaround_string,
        "num_booster_reflights": num_booster_reflights,
        "num_ship_reflights": num_ship_reflights,
        "starship_reflights": starship_reflights,
        "pad_stats": pad_stats,
        "zone_stats": recovery_zone_stats,
    }
    return render(request, "starship/starship_home.html", context=context)


def starship_booster_list(request):
    super_heavies = Stage.objects.filter(
        rocket__family__provider__name="SpaceX",
        type="BOOSTER",
        rocket__name__icontains="Starship",
    )

    active_boosters = super_heavies.filter(status="ACTIVE").order_by("name")
    lost_boosters = super_heavies.filter(Q(status="LOST") | Q(status="EXPENDED")).order_by("name")
    retired_boosters = super_heavies.filter(status="RETIRED").order_by("name")

    context = {
        "active_boosters": active_boosters,
        "retired_boosters": retired_boosters,
        "lost_boosters": lost_boosters,
    }

    return render(request, "boosters/booster_list.html", context)
