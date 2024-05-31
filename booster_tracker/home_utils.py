from django.db.models import Q, Count, Max
from booster_tracker.models import Stage, StageAndRecovery, Pad, PadUsed, Boat, Rocket, LandingZone, Launch
from booster_tracker.utils import concatenated_list, convert_seconds, TurnaroundObjects
from datetime import datetime
import pytz
from enum import StrEnum


class StageObjects(StrEnum):
    BOOSTER = "BOOSTER"
    SECOND_STAGE = "SECOND_STAGE"


def get_most_flown_stages(rocket_name: str, stage_type: StageObjects):
    """Returns the booster(s) with the highest number of flights, and how many flights that is"""
    booster_and_launch_count = Stage.objects.filter(
        stageandrecovery__launch__time__lte=datetime.now(pytz.utc),
        type=stage_type,
        rocket__name__icontains=rocket_name,
    ).annotate(launch_count=Count("stageandrecovery__launch", distinct=True))

    max_launch_count = booster_and_launch_count.aggregate(Max("launch_count"))["launch_count__max"]

    most_flown_boosters = list(
        booster_and_launch_count.filter(launch_count=max_launch_count).values_list("name", flat=True)
    )

    return (most_flown_boosters, max_launch_count)


def get_landings_and_successes(rocket_name: str) -> tuple:
    """Returns number of landing attempts and number of successful landings"""
    num_landing_attempts = (
        StageAndRecovery.objects.filter(
            launch__time__lte=datetime.now(pytz.utc),
            stage__rocket__name__icontains=rocket_name,
        )
        .filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
        .filter(~Q(method_success="PRECLUDED"))
        .count()
    )

    num_successes = (
        StageAndRecovery.objects.filter(
            launch__time__lte=datetime.now(pytz.utc),
            method_success="SUCCESS",
            stage__rocket__name__icontains=rocket_name,
        )
        .filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
        .count()
    )

    return (num_landing_attempts, num_successes)


def get_next_and_last_launches():
    """Gets the next launch and last launch"""
    next_launch = Launch.objects.filter(time__gt=datetime.now(pytz.utc)).last()
    last_launch = Launch.objects.filter(time__lte=datetime.now(pytz.utc)).first()
    return next_launch, last_launch


def gather_launch_info(launch):
    if launch.time > datetime.now(pytz.utc):
        boosters = launch.boosters.replace("N/A", "Unknown") if launch else "TBD"
        recoveries = launch.recoveries if launch else "TBD"
        photo = (
            PadUsed.objects.get(pad=launch.pad, rocket=launch.rocket).image.url
            if launch
            else "rocket_pad_photos/rocket_launch_image.jpg"
        )
    else:
        boosters = launch.boosters
        recoveries = launch.recoveries
        photo = None  # No photo needed for the last launch

    tugs = concatenated_list(
        list(Boat.objects.filter(type="TUG", tugonlaunch__launch=launch).all().values_list("name", flat=True))
    )
    fairing_recovery = concatenated_list(
        list(
            set(
                Boat.objects.filter(type="FAIRING_RECOVERY", fairingrecovery__launch=launch)
                .all()
                .values_list("name", flat=True)
            )
        )
    )
    return boosters, recoveries, tugs, fairing_recovery, photo


def gather_stats(last_launch):
    """Returns stats for the home page"""
    num_launches_per_rocket_and_successes = []
    for rocket in Rocket.objects.filter(family__provider__name="SpaceX"):
        num_launches_per_rocket_and_successes.append([rocket.name, rocket.num_launches, rocket.num_successes])

    num_landings_and_successes = get_landings_and_successes(rocket_name="Falcon")
    most_flown_boosters = get_most_flown_stages(rocket_name="Falcon", stage_type=StageObjects.BOOSTER)
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

    return {
        "num_launches_per_rocket_and_successes": num_launches_per_rocket_and_successes,
        "num_landings_and_successes": num_landings_and_successes,
        "most_flown_boosters_string": most_flown_boosters_string,
        "quickest_booster_turnaround_string": quickest_booster_turnaround_string,
        "shortest_time_between_launches": shortest_time_between_launches,
        "num_booster_reflights": num_booster_reflights,
        "falcon_9_reflights": falcon_9_reflights,
        "falcon_heavy_reflights": falcon_heavy_reflights,
    }


def gather_pad_stats(rocket_name):
    pad_stats = []
    for pad in (
        Pad.objects.filter(
            padused__rocket__name__icontains=rocket_name,
            padused__rocket__family__provider__name="SpaceX",
        )
        .distinct()
        .order_by("id")
    ):
        num_landings = pad.num_launches
        fastest_turnaround = pad.fastest_turnaround
        pad_stats.append([pad, num_landings, fastest_turnaround])
    return pad_stats


def gather_recovery_zone_stats(rocket_name):
    recovery_zone_stats = []
    for zone in (
        LandingZone.objects.filter(
            stageandrecovery__stage__rocket__family__provider__name="SpaceX",
            stageandrecovery__stage__rocket__name__icontains=rocket_name,
        )
        .distinct()
        .order_by("id")
    ):
        num_landings = zone.num_landings
        fastest_turnaround = zone.fastest_turnaround
        recovery_zone_stats.append([zone, num_landings, fastest_turnaround])
    return recovery_zone_stats


# This section is for the Starship home page
def get_last_starship_launch():
    return Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Starship").first()


def gather_launch_stats(rocket_name):
    num_launches_per_rocket_and_successes = []
    for rocket in Rocket.objects.filter(family__provider__name="SpaceX", name=rocket_name):
        num_launches_per_rocket_and_successes.append([rocket.name, rocket.num_launches, rocket.num_successes])
    return num_launches_per_rocket_and_successes


def gather_landing_stats(rocket_name):
    ship_landing_attempts = (
        StageAndRecovery.objects.filter(stage__rocket__name=rocket_name, stage__type="SECOND_STAGE")
        .filter((Q(method="DRONE_SHIP") | Q(method="GROUND_PAD") | Q(method="CATCH")))
        .count()
    )

    ship_landing_successes = (
        StageAndRecovery.objects.filter(
            stage__rocket__name=rocket_name,
            stage__type="SECOND_STAGE",
            method_success="SUCCESS",
        )
        .filter((Q(method="DRONE_SHIP") | Q(method="GROUND_PAD") | Q(method="CATCH")))
        .count()
    )

    booster_landing_attempts = (
        StageAndRecovery.objects.filter(stage__rocket__name=rocket_name, stage__type="BOOSTER")
        .filter((Q(method="DRONE_SHIP") | Q(method="GROUND_PAD") | Q(method="CATCH")))
        .count()
    )

    booster_landing_successes = (
        StageAndRecovery.objects.filter(
            stage__rocket__name=rocket_name,
            stage__type="BOOSTER",
            method_success="SUCCESS",
        )
        .filter((Q(method="DRONE_SHIP") | Q(method="GROUND_PAD") | Q(method="CATCH")))
        .count()
    )
    return {
        "ship_landing_attempts": ship_landing_attempts,
        "ship_landing_successes": ship_landing_successes,
        "booster_landing_attempts": booster_landing_attempts,
        "booster_landing_successes": booster_landing_successes,
    }


def gather_most_flown_stages(rocket_name):
    most_flown_boosters = get_most_flown_stages(rocket_name=rocket_name, stage_type=StageObjects.BOOSTER)
    most_flown_ships = get_most_flown_stages(rocket_name=rocket_name, stage_type=StageObjects.SECOND_STAGE)

    most_flown_boosters_string = f"{concatenated_list(most_flown_boosters[0])}; {most_flown_boosters[1]} flights"
    most_flown_ships_string = f"{concatenated_list(most_flown_ships[0])}; {most_flown_ships[1]} flights"

    return most_flown_boosters_string, most_flown_ships_string


def get_quickest_turnaround(last_launch, stage_type):
    if not last_launch:
        return "N/A"
    turnarounds = last_launch.calculate_turnarounds(turnaround_object=stage_type)
    if not turnarounds:
        return "N/A"
    starship_turnarounds = [
        row for row in turnarounds["ordered_turnarounds"] if "Starship" in row["turnaround_object"].rocket.name
    ]
    if not starship_turnarounds:
        return "N/A"
    return f"{starship_turnarounds[0]['turnaround_object']} at {convert_seconds(starship_turnarounds[0]['turnaround_time'])}"


def gather_reflights_stats(rocket_name):
    num_booster_uses = (
        StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc), stage__type=StageObjects.BOOSTER)
        .filter(launch__rocket__name__icontains=rocket_name)
        .count()
    )
    num_boosters_used = (
        Stage.objects.filter(
            type=StageObjects.BOOSTER,
            stageandrecovery__launch__time__lte=datetime.now(pytz.utc),
        )
        .filter(rocket__name__icontains=rocket_name)
        .distinct()
        .count()
    )
    num_booster_reflights = num_booster_uses - num_boosters_used

    num_ship_uses = (
        StageAndRecovery.objects.filter(
            launch__time__lte=datetime.now(pytz.utc),
            stage__type=StageObjects.SECOND_STAGE,
        )
        .filter(launch__rocket__name__icontains=rocket_name)
        .count()
    )
    num_ships_used = (
        Stage.objects.filter(
            type=StageObjects.SECOND_STAGE,
            stageandrecovery__launch__time__lte=datetime.now(pytz.utc),
        )
        .filter(rocket__name__icontains=rocket_name)
        .distinct()
        .count()
    )
    num_ship_reflights = num_ship_uses - num_ships_used

    return num_booster_reflights, num_ship_reflights


def get_starship_reflights():
    return (
        Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Starship")
        .first()
        .get_rocket_flights_reused_vehicle()
    )
