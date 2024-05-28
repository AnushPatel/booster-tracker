from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from booster_tracker.utils import concatenated_list, TurnaroundObjects, convert_seconds
from booster_tracker.home_utils import (
    get_landings_and_successes,
    get_most_flown_stages,
    StageObjects,
)

import pytz
import statistics
from datetime import datetime

from .models import (
    PadUsed,
    Boat,
    Rocket,
    Stage,
    StageAndRecovery,
    Pad,
    LandingZone,
    Launch,
    Spacecraft,
    SpacecraftOnLaunch,
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
    next_launch = Launch.objects.filter(time__gt=datetime.now(pytz.utc)).last()
    last_launch = Launch.objects.filter(time__lte=datetime.now(pytz.utc)).first()

    # Gather all needed information to create next launch card
    if next_launch:
        next_launch_boosters = next_launch.boosters.replace("N/A", "Unknown")
        next_launch_recoveries = next_launch.recoveries
        next_launch_photo = PadUsed.objects.get(pad=next_launch.pad, rocket=next_launch.rocket).image.url
    else:
        next_launch_boosters = "TBD"
        next_launch_recoveries = "TBD"
        next_launch_photo = "rocket_pad_photos/rocket_launch_image.jpg"

    next_launch_tugs = concatenated_list(
        list(Boat.objects.filter(type="TUG", tugonlaunch__launch=next_launch).all().values_list("name", flat=True))
    )
    next_launch_fairing_recovery = concatenated_list(
        list(
            set(
                Boat.objects.filter(type="FAIRING_RECOVERY", fairingrecovery__launch=next_launch)
                .all()
                .values_list("name", flat=True)
            )
        )
    )

    # Gather all needed information to create last launch card
    last_launch_boosters = last_launch.boosters
    last_launch_recoveries = last_launch.recoveries
    last_launch_tugs = concatenated_list(
        list(Boat.objects.filter(type="TUG", tugonlaunch__launch=last_launch).all().values_list("name", flat=True))
    )
    last_launch_fairing_recovery = concatenated_list(
        list(
            set(
                Boat.objects.filter(type="FAIRING_RECOVERY", fairingrecovery__launch=last_launch)
                .all()
                .values_list("name", flat=True)
            )
        )
    )

    # Gather information needed for all of the stats
    num_launches_per_rocket_and_successes = []
    for rocket in Rocket.objects.filter(provider__name="SpaceX"):
        num_launches_per_rocket_and_successes.append([rocket.name, rocket.num_launches, rocket.num_successes])

    num_landings_and_successes = get_landings_and_successes(rocket_name="Falcon")
    most_flown_boosters = get_most_flown_stages(rocket_name="Falcon", type=StageObjects.BOOSTER)

    most_flown_boosters_string = f"{concatenated_list(most_flown_boosters[0])}; {most_flown_boosters[1]} flights"

    booster_turnarounds = last_launch.calculate_turnarounds(turnaround_object=TurnaroundObjects.BOOSTER)

    falcon_booster_turnarounds = [
        row for row in booster_turnarounds["ordered_turnarounds"] if "Falcon" in row["turnaround_object"].rocket.name
    ]

    quickest_booster_turnaround_string = f"{falcon_booster_turnarounds[0]['turnaround_object']} at {convert_seconds(falcon_booster_turnarounds[0]['turnaround_time'])}"
    shortest_time_between_launches = convert_seconds(
        last_launch.calculate_turnarounds(turnaround_object=TurnaroundObjects.ALL)["ordered_turnarounds"][0][
            "turnaround_time"
        ]
    )

    # this section gets total number of reflights; it takes the number of booster uses and subtracts the number of boosters that have flown
    num_booster_uses = (
        StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc))
        .filter(launch__rocket__name__icontains="Falcon")
        .count()
    )
    num_stages_used = (
        Stage.objects.filter(type="BOOSTER", stageandrecovery__launch__time__lte=datetime.now(pytz.utc))
        .filter(rocket__name__icontains="Falcon")
        .distinct()
        .count()
    )
    num_booster_reflights = num_booster_uses - num_stages_used

    falcon_9_reflights = (
        Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Falcon 9")
        .first()
        .get_rocket_flights_reused_vehicle()
    )
    falcon_heavy_reflights = (
        Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Falcon Heavy")
        .first()
        .get_rocket_flights_reused_vehicle()
    )

    pad_stats: list = []
    for pad in (
        Pad.objects.filter(
            padused__rocket__name__icontains="Falcon",
            padused__rocket__provider__name="SpaceX",
        )
        .distinct()
        .order_by("id")
    ):
        num_landings = pad.num_launches
        fastest_turnaround = pad.fastest_turnaround
        pad_stats.append([pad, num_landings, fastest_turnaround])

    recovery_zone_stats: list = []
    for zone in (
        LandingZone.objects.filter(
            stageandrecovery__stage__rocket__provider__name="SpaceX",
            stageandrecovery__stage__rocket__name__icontains="Falcon",
        )
        .distinct()
        .order_by("id")
    ):
        num_landings = zone.num_landings
        fastest_turnaround = zone.fastest_turnaround
        recovery_zone_stats.append([zone, num_landings, fastest_turnaround])

    context = {
        "launches_per_vehicle": num_launches_per_rocket_and_successes,
        "num_landings": num_landings_and_successes,
        "num_booster_reflights": num_booster_reflights,
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
        "most_flown_boosters": most_flown_boosters_string,
        "quickest_booster_turnaround": quickest_booster_turnaround_string,
        "falcon_heavy_reflights": falcon_heavy_reflights,
        "falcon_9_reflights": falcon_9_reflights,
        "pad_stats": pad_stats,
        "zone_stats": recovery_zone_stats,
        "shortest_time_between_launches": shortest_time_between_launches,
    }
    return render(request, "launches/home.html", context=context)


def launch_details(request, launch_name):
    launch = get_object_or_404(Launch, name=launch_name)
    context = {"data": launch.create_launch_table(), "launch": launch}
    return render(request, "launches/launch_table.html", context)


def booster_list(request):
    falcon_boosters = Stage.objects.filter(
        rocket__provider__name="SpaceX",
        type="BOOSTER",
        rocket__name__icontains="Falcon",
    )

    active_boosters = falcon_boosters.filter(status="ACTIVE").order_by("name")
    lost_boosters = falcon_boosters.filter(Q(status="LOST") | Q(status="EXPENDED")).order_by("name")
    retired_boosters = falcon_boosters.filter(status="RETIRED").order_by("name")

    context = {
        "active_boosters": active_boosters,
        "retired_boosters": retired_boosters,
        "lost_boosters": lost_boosters,
    }

    return render(request, "boosters/booster_list.html", context)


def booster_info(request, booster_name):
    booster = get_object_or_404(Stage, name=booster_name, rocket__name__icontains="Falcon")
    launches = Launch.objects.filter(stageandrecovery__stage=booster).order_by("time")
    launches_information = []
    turnarounds = []

    for launch in launches:
        turnaround = launch.get_stage_flights_and_turnaround(stage=booster)[1]
        launches_information.append(
            [
                launch,
                turnaround,
                StageAndRecovery.objects.get(launch=launch, stage=booster),
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
        "booster": booster,
        "launches": launches_information,
        "average_turnaround": average_turnaround,
        "stdev": turnaround_stdev,
        "quickest_turnaround": quickest_turnaround,
    }

    return render(request, "boosters/booster_info.html", context)


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


""" def starship_home(request):
    # Gather information needed for all of the stats
    num_launches_per_rocket_and_successes = []
    for rocket in Rocket.objects.filter(provider__name="SpaceX"):
        num_launches_per_rocket_and_successes.append(
            [rocket.name, rocket.num_launches, rocket.num_successes]
        )

    ship_landing_attempts = (
        StageAndRecovery.objects.filter(
            stage__rocket__name="Starship", stage__type="SECOND_STAGE"
        )
        .filter((Q(method="DRONE_SHIP") | Q(method="GROUND_PAD" | Q(method="CATCH"))))
        .count()
    )

    ship_landing_successes = (
        StageAndRecovery.objects.filter(
            stage__rocket__name="Starship",
            stage__type="SECOND_STAGE",
            method_success="SUCCESS",
        )
        .filter((Q(method="DRONE_SHIP") | Q(method="GROUND_PAD" | Q(method="CATCH"))))
        .count()
    )

    booster_landing_attempts = (
        StageAndRecovery.objects.filter(
            stage__rocket__name="Starship", stage__type="BOOSTER"
        )
        .filter((Q(method="DRONE_SHIP") | Q(method="GROUND_PAD" | Q(method="CATCH"))))
        .count()
    )

    booster_landing_successes = (
        StageAndRecovery.objects.filter(
            stage__rocket__name="Starship",
            stage__type="BOOSTER",
            method_success="SUCCESS",
        )
        .filter((Q(method="DRONE_SHIP") | Q(method="GROUND_PAD" | Q(method="CATCH"))))
        .count()
    )

    most_flown_boosters = get_most_flown_stages(
        rocket_name="Starship", type=StageObjects.BOOSTER
    )
    most_flown_ships = get_most_flown_stages(
        rocket_name="Starship", type=StageObjects.SECOND_STAGE
    )

    most_flown_boosters_string = (
        f"{concatenated_list(most_flown_boosters[0])}; {most_flown_boosters[1]} flights"
    )

    most_flown_stages_string = (
        f"{concatenated_list(most_flown_ships[0])}; {most_flown_ships[1]} flights"
    )

    starship_turnarounds = [
        row
        for row in starship_turnarounds["ordered_turnarounds"]
        if "Starship" in row["turnaround_object"].rocket.name
    ]

    starship_booster_turnarounds = [
        row
        for row in starship_turnarounds["ordered_turnarounds"]
        if "BOOSTER" == row["turnaround_object"].type
    ]

    starship_ship_turnarounds = [
        row
        for row in starship_turnarounds["ordered_turnarounds"]
        if "SECOND_STAGE" == row["turnaround_object"].type
    ]

    quickest_booster_turnaround_string = f"{starship_booster_turnarounds[0]['turnaround_object']} at {convert_seconds(starship_booster_turnarounds[0]['turnaround_time'])}"
    quickest_ship_turnaround_string = f"{starship_ship_turnarounds[0]['turnaround_object']} at {convert_seconds(starship_ship_turnarounds[0]['turnaround_time'])}"

    # this section gets total number of reflights; it takes the number of booster uses and subtracts the number of boosters that have flown
    num_booster_uses = (
        StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc))
        .filter(launch__rocket__name__icontains="Starship")
        .count()
    )
    num_stages_used = (
        Stage.objects.filter(
            type=StageObjects.BOOSTER,
            stageandrecovery__launch__time__lte=datetime.now(pytz.utc),
        )
        .filter(rocket__name__icontains="Starship")
        .distinct()
        .count()
    )
    num_booster_reflights = num_booster_uses - num_stages_used

    num_ship_uses = (
        StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc))
        .filter(launch__rocket__name__icontains="Starship")
        .count()
    )
    num_ships_used = (
        Stage.objects.filter(
            type=StageObjects.SECOND_STAGE,
            stageandrecovery__launch__time__lte=datetime.now(pytz.utc),
        )
        .filter(rocket__name__icontains="Starship")
        .distinct()
        .count()
    )
    num_ship_reflights = num_ship_uses - num_ships_used

    starship_reflights = (
        Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Starship")
        .first()
        .get_rocket_flights_reused_vehicle()
    )

    pad_stats: list = []
    for pad in (
        Pad.objects.filter(
            padused__rocket__name__icontains="Falcon",
            padused__rocket__provider__name="SpaceX",
        )
        .distinct()
        .order_by("id")
    ):
        num_landings = pad.num_launches
        fastest_turnaround = pad.fastest_turnaround
        pad_stats.append([pad, num_landings, fastest_turnaround])

    recovery_zone_stats: list = []
    for zone in (
        LandingZone.objects.filter(
            stageandrecovery__stage__rocket__provider__name="SpaceX",
            stageandrecovery__stage__rocket__name__icontains="Falcon",
        )
        .distinct()
        .order_by("id")
    ):
        num_landings = zone.num_landings
        fastest_turnaround = zone.fastest_turnaround
        recovery_zone_stats.append([zone, num_landings, fastest_turnaround])

    context = {
        "launches_per_vehicle": num_launches_per_rocket_and_successes,
        "num_landings": num_landings_and_successes,
        "num_booster_reflights": num_booster_reflights,
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
        "most_flown_boosters": most_flown_boosters_string,
        "quickest_booster_turnaround": quickest_booster_turnaround_string,
        "falcon_heavy_reflights": falcon_heavy_reflights,
        "falcon_9_reflights": falcon_9_reflights,
        "pad_stats": pad_stats,
        "zone_stats": recovery_zone_stats,
        "shortest_time_between_launches": shortest_time_between_launches,
    }
    return render(request, "launches/home.html", context=context) """
