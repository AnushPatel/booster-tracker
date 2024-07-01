from django.db.models import Q, Count, Max
from booster_tracker.models import (
    Stage,
    StageAndRecovery,
    Pad,
    PadUsed,
    Boat,
    Rocket,
    LandingZone,
    Launch,
    RocketFamily,
    Spacecraft,
    SpacecraftFamily,
)
from booster_tracker.utils import concatenated_list, convert_seconds, TurnaroundObjects
from datetime import datetime
from django.templatetags.static import static
import pytz
from enum import StrEnum
from collections import defaultdict


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
    if launch and launch.time > datetime.now(pytz.utc):
        boosters = launch.boosters.replace("N/A", "Unknown")
        recoveries = launch.recoveries
        photo = PadUsed.objects.get(pad=launch.pad, rocket=launch.rocket).image.url
    elif launch:
        boosters = launch.boosters
        recoveries = launch.recoveries
        photo = None  # No photo needed for the last launch
    else:
        boosters = "TBD"
        recoveries = "TBD"
        photo = "rocket_pad_photos/rocket_launch_image.jpg"

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

    if last_launch:
        booster_turnarounds = last_launch.calculate_turnarounds(turnaround_object=TurnaroundObjects.BOOSTER)
        if booster_turnarounds:
            falcon_booster_turnarounds = [
                row
                for row in booster_turnarounds["ordered_turnarounds"]
                if "Falcon" in row["turnaround_object"].rocket.name
            ]
            quickest_booster_turnaround_string = f"{falcon_booster_turnarounds[0]['turnaround_object']} at {convert_seconds(falcon_booster_turnarounds[0]['turnaround_time'])}"
            shortest_time_between_launches = convert_seconds(
                last_launch.calculate_turnarounds(turnaround_object=TurnaroundObjects.ALL)["ordered_turnarounds"][0][
                    "turnaround_time"
                ]
            )
        else:
            quickest_booster_turnaround_string = "No data"
            shortest_time_between_launches = "No data"
    else:
        booster_turnarounds = {"ordered_turnarounds": []}
        falcon_booster_turnarounds = []
        quickest_booster_turnaround_string = "No data"
        shortest_time_between_launches = "No data"

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

    if launch := (Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Falcon 9").first()):
        falcon_9_reflights = launch.get_rocket_flights_reused_vehicle()
    else:
        falcon_9_reflights = 0

    if launch := (Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Falcon Heavy").first()):
        falcon_heavy_reflights = launch.get_rocket_flights_reused_vehicle()
    else:
        falcon_heavy_reflights = 0

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


def generate_home_page():
    next_launch, last_launch = get_next_and_last_launches()

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

    return context


def generate_boosters_page(rocket_family: RocketFamily, stage_type):
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

    return context


def generate_starship_home():
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

    return context


def generate_spacecraft_list(family: Spacecraft):
    spacecraft = Spacecraft.objects.filter(family__name=family)

    active_spacecraft = spacecraft.filter(status="ACTIVE").order_by("name")
    lost_spacecraft = spacecraft.filter(Q(status="LOST") | Q(status="EXPENDED")).order_by("name")
    retired_spacecraft = spacecraft.filter(status="RETIRED").order_by("name")

    context = {
        "active_spacecraft": active_spacecraft,
        "retired_spacecraft": retired_spacecraft,
        "lost_spacecraft": lost_spacecraft,
    }

    return context


# This section deals with functions that are used by the API
def combine_dicts(dict1, dict2):
    combined = defaultdict(list)

    for key, value in dict1.items():
        combined[key].extend(value)

    if dict2:
        for key, value in dict2.items():
            combined[key].extend(value)

    for key in combined:
        combined[key] = list(set(combined[key]))

    return dict(combined)


def get_true_filter_values(filter, filter_item):
    true_values = {}

    for value in filter[filter_item].values():
        if isinstance(value, dict):
            # If the value is a dict, need to go one layer further in to get the data. Ex: {"rocket__family": {"rocket": {"1": True, "2": True}}} should look at "rockets" since this contains all information about parent filter
            for child_filter_item in filter[filter_item].keys():
                true_values = combine_dicts(true_values, get_true_filter_values(filter[filter_item], child_filter_item))
        else:
            # If there is not a dict, then find the values which are true
            true_values_for_filter_name = []
            for key, value in filter[filter_item].items():
                if value:
                    # If the string is an int, convert it for query purposes. Strings vs int determined by database storage type
                    formatted_key = lambda key: (int(key) if key.isnumeric() else key)
                    true_values_for_filter_name.append(formatted_key(key))
            true_values[filter_item] = true_values_for_filter_name

    return true_values


def get_launches_with_filter(filter: dict, query: str = ""):
    """Takes in a filter and returns all launch objects that obey one of those filters"""
    true_values = {}

    for filter_item in filter.keys():
        # Cycles through filter to get all values that are true into a list; ex {"rocket": {"1": True, "2": False, "3": True}} => {"rocket": [1, 2, 3]}
        true_values_from_item = get_true_filter_values(filter, filter_item)
        true_values = true_values | true_values_from_item

    non_ids = ["launch_outcome"]

    print(true_values)

    q_objects = Q()
    for key, value in true_values.items():
        if key in non_ids:
            q_objects &= Q(**{f"{key}__in": value})
        else:
            q_objects &= Q(**{f"{key}__id__in": value})  # Create and kwarg for filtering purposes

    filtered_launches = Launch.objects.filter(q_objects).filter(name__icontains=query).distinct()
    return filtered_launches


def launches_per_day(launches: list[Launch]):
    """Takes in a list of launches and gives the number of launches on each day (excluding year)"""
    launches_per_day = defaultdict(int)
    for launch in launches:
        date = f"{launch.time.strftime('%B %d')}"
        launches_per_day[date] += 1

    launches_per_day = sorted(launches_per_day.items(), key=lambda x: x[1], reverse=True)

    return launches_per_day
