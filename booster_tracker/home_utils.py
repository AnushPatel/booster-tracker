from django.db.models import Q, Count, Max
from booster_tracker.models import Stage, StageAndRecovery, Rocket
from datetime import datetime
import pytz
from enum import StrEnum


class StageObjects(StrEnum):
    BOOSTER = "BOOSTER"
    SECOND_STAGE = "SECOND_STAGE"


def get_most_flown_stages(rocket_name: str, type: StrEnum):
    """Returns the booster(s) with the highest number of flights, and how many flights that is"""
    booster_and_launch_count = Stage.objects.filter(
        stageandrecovery__launch__time__lte=datetime.now(pytz.utc),
        type=type,
        rocket__name__icontains=rocket_name,
    ).annotate(launch_count=Count("stageandrecovery__launch", distinct=True))

    max_launch_count = booster_and_launch_count.aggregate(Max("launch_count"))[
        "launch_count__max"
    ]

    most_flown_boosters = list(
        booster_and_launch_count.filter(launch_count=max_launch_count).values_list(
            "name", flat=True
        )
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
