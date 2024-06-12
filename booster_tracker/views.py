from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
import urllib.parse
from booster_tracker.home_utils import (
    generate_home_page,
    generate_starship_home,
    generate_boosters_page,
    generate_spacecraft_list,
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
    SpacecraftFamily,
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
        return render(request, "launches/home.html", cached_content)

    context = generate_home_page()
    cache.set(cache_key, context, timeout=None)

    return render(request, "launches/home.html", context)


def launch_details(request, encoded_launch_name):
    launch_name = urllib.parse.unquote(encoded_launch_name)
    launch = get_object_or_404(Launch, name=launch_name)
    context = {"data": launch.create_launch_table(), "launch": launch}
    return render(request, "launches/launch_table.html", context)


def stage_list(request, rocket_family_name: str, stage_type):
    rocket_family = RocketFamily.objects.get(name__icontains=rocket_family_name)
    cache_key = f"{rocket_family.name.lower()}_boosters"
    cached_content = cache.get(cache_key)

    if cached_content:
        return render(request, "stages/stage_list.html", cached_content)

    context = generate_boosters_page(rocket_family=rocket_family, stage_type=stage_type)
    cache.set(cache_key, context, timeout=None)

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
    cache_key = "Dragons"
    cached_content = cache.get(cache_key)

    if cached_content:
        return render(request, "dragons/dragon_list.html", cached_content)

    context = generate_spacecraft_list(SpacecraftFamily.objects.get(name="Dragon"))
    cache.set(cache_key, context, timeout=None)

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
    cache_key = "starship_home"
    cached_content = cache.get(cache_key)

    if cached_content:
        return render(request, "starship/starship_home.html", cached_content)

    context = generate_starship_home()
    cache.set(cache_key, context, timeout=None)

    return render(request, "starship/starship_home.html", context)


def health(request):
    return HttpResponse("Success", status=200)
