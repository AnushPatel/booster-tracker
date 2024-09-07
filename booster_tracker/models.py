from django.db import models
from booster_tracker.utils import (
    make_ordinal,
    concatenated_list,
    TurnaroundObjects,
    success,
    convert_seconds,
    format_time,
    turnaround_time,
    is_significant,
)
from datetime import datetime
from django.db.models import Q
from django.urls import reverse
from colorfield.fields import ColorField
import pytz
import urllib.parse
import random

# Choices for fields
RECOVERY_METHODS = [
    ("EXPENDED", "expended"),
    ("OCEAN_SURFACE", "ocean"),
    ("DRONE_SHIP", "ASDS"),
    ("GROUND_PAD", "landing zone"),
    ("PARACHUTE", "parachute"),
    ("CATCH", "catch"),
]
LAUNCH_OUTCOMES = [
    ("SUCCESS", "success"),
    ("FAILURE", "failure"),
    ("PARTIAL FAILURE", "partial failure"),
]
LANDING_METHOD_OUTCOMES = [
    ("SUCCESS", "success"),
    ("FAILURE", "failure"),
    ("PRECLUDED", "precluded"),
]
BOAT_TYPES = [
    ("TUG", "tug"),
    ("FAIRING_RECOVERY", "fairing recovery"),
    ("SUPPORT", "support"),
    ("SPACECRAFT_RECOVERY", "spacecraft recovery"),
]
STAGE_TYPES = [("BOOSTER", "booster"), ("SECOND_STAGE", "second stage")]
SPACECRAFT_TYPES = [("CARGO", "cargo"), ("CREW", "crew")]
STAGE_LIFE_OPTIONS = [
    ("ACTIVE", "active"),
    ("RETIRED", "retired"),
    ("EXPENDED", "expended"),
    ("LOST", "lost"),
]
LIFE_OPTIONS = [("ACTIVE", "active"), ("RETIRED", "retired")]
BOOSTER_TYPES = [
    ("MY", "MY"),
    ("PY", "PY"),
    ("CENTER", "center"),
    ("SINGLE_CORE", "single core"),
]

# Create models:


class Operator(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RocketFamily(models.Model):
    name = models.CharField(max_length=100, unique=True)
    provider = models.ForeignKey(Operator, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Rocket Families"


class Rocket(models.Model):
    name = models.CharField(max_length=100, unique=True)
    family = models.ForeignKey(RocketFamily, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=LIFE_OPTIONS, default="ACTIVE")
    color = ColorField(default="#218243")

    def __str__(self):
        return self.name

    @property
    def num_launches(self):
        """Returns number of launches"""
        return Launch.objects.filter(rocket=self, time__lte=datetime.now(pytz.utc)).count()

    @property
    def num_successes(self):
        """Returns number of successful launches"""
        return Launch.objects.filter(rocket=self, launch_outcome="SUCCESS", time__lte=datetime.now(pytz.utc)).count()


class Stage(models.Model):
    name = models.CharField(max_length=50)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    version = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=STAGE_TYPES)
    image = models.ImageField(upload_to="stage_photos/", default="stage_photos/default_booster.jpg")
    credit = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STAGE_LIFE_OPTIONS, default="ACTIVE")

    def __str__(self):
        return self.name

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "rocket"], name="unique_rocket_stage")]

    @property
    def num_launches(self):
        return StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc), stage=self).count()

    @property
    def fastest_turnaround(self):
        """Function returns fastest turnaround of booster in string form (ex: 12 days, 4 hours, and 3 minutes)"""
        fastest_turnaround = "N/A"

        if launch := Launch.objects.filter(time__lte=datetime.now(pytz.utc), stageandrecovery__stage=self).first():
            turnarounds = launch.calculate_turnarounds(turnaround_object=TurnaroundObjects.BOOSTER)
            if turnarounds:
                specific_stage_turnarounds = [
                    row for row in turnarounds["ordered_turnarounds"] if self == row["turnaround_object"]
                ]
                if len(specific_stage_turnarounds) > 0:
                    fastest_turnaround = convert_seconds(specific_stage_turnarounds[0]["turnaround_time"])

        return fastest_turnaround


class SpacecraftFamily(models.Model):
    name = models.CharField(max_length=200, unique=True)
    provider = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=200, choices=LIFE_OPTIONS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Spacecraft Families"


class Spacecraft(models.Model):
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, choices=SPACECRAFT_TYPES)
    family = models.ForeignKey(SpacecraftFamily, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=50, choices=STAGE_LIFE_OPTIONS, default="ACTIVE")
    image = models.ImageField(upload_to="spacecraft_photos/", default="spacecraft_photos/default_dragon.jpg")
    credit = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "family"], name="unique_family_name")]

    @property
    def num_launches(self):
        return SpacecraftOnLaunch.objects.filter(launch__time__lte=datetime.now(pytz.utc), spacecraft=self).count()


class Boat(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=BOAT_TYPES)
    status = models.CharField(max_length=50, choices=LIFE_OPTIONS, default="ACTIVE")

    def __str__(self):
        return self.name

    class Meta:
        constraints = [models.UniqueConstraint(fields=["name", "type"], name="unique_boat_name_type")]


class Orbit(models.Model):
    name = models.CharField(max_length=200, unique=True)
    nickname = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.name


class Pad(models.Model):
    name = models.CharField(max_length=200, unique=True)
    nickname = models.CharField(max_length=25)
    location = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=LIFE_OPTIONS, default="ACTIVE")
    image = models.ImageField(upload_to="pad_photos/", default="media/pad_photos/default.png")
    credit = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nickname

    @property
    def num_launches(self):
        return Launch.objects.filter(pad=self, time__lte=datetime.now(pytz.utc)).count()

    @property
    def fastest_turnaround(self):
        """Returns the fastest turnaround of landing zone"""
        if (
            launch := Launch.objects.filter(time__lte=datetime.now(pytz.utc), pad=self)
            .order_by("pad_turnaround")
            .first()
        ):
            if launch is None or launch.pad_turnaround is None:
                return "N/A"
            return convert_seconds(launch.pad_turnaround)

        return "N/A"


class Launch(models.Model):
    time = models.DateTimeField("Launch Time")
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    orbit = models.ForeignKey(Orbit, on_delete=models.CASCADE, null=True, blank=True)
    mass = models.IntegerField(blank=True, null=True, verbose_name="Mass (kg)")
    customer = models.CharField(max_length=200)
    launch_outcome = models.CharField(max_length=200, choices=LAUNCH_OUTCOMES, blank=True, null=True)
    pad_turnaround = models.IntegerField(blank=True, null=True, editable=False)
    company_turnaround = models.IntegerField(blank=True, null=True, editable=False)
    image = models.CharField(max_length=200, blank=True, null=True, editable=False)
    stages_string = models.CharField(max_length=500, blank=True, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Launches"
        ordering = ["-time"]

    def __str__(self):
        return self.name

    _from_task = False

    @property
    def get_image(self) -> str:
        """Returns the image url stored in database"""
        return PadUsed.objects.get(pad=self.pad, rocket=self.rocket).image.url

    @property
    def droneship_needed(self) -> bool:
        """Returns bool of if a droneship was needed/used on launch"""
        return StageAndRecovery.objects.filter(launch=self, method="DRONE_SHIP").exists()

    @property
    def flight_proven_booster(self) -> bool:
        """Returns bool of if any booster on the launch was flight prover"""
        return StageAndRecovery.objects.filter(launch=self, num_flights__gt=1).exists()

    @property
    def num_successful_landings(self) -> int:
        """Returns number of successful landings on the launch; all landings are assumed successful if in future"""
        if self.time > datetime.now(pytz.utc):
            return (
                StageAndRecovery.objects.filter(launch=self, stage__type="BOOSTER", method_success="SUCCESS")
                .filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
                .count()
            )
        return (
            StageAndRecovery.objects.filter(launch=self, stage__type="BOOSTER")
            .filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
            .count()
        )

    @property
    def encoded_name(self):
        return urllib.parse.quote(self.name, safe="")

    @property
    def get_company_turnaround(self):
        if (
            last_launch := Launch.objects.filter(
                rocket__family__provider=self.rocket.family.provider, time__lt=self.time
            )
            .order_by("time")
            .last()
        ):
            return (self.time - last_launch.time).total_seconds()
        return None

    @property
    def get_pad_turnaround(self):
        if last_launch := Launch.objects.filter(pad=self.pad, time__lt=self.time).order_by("time").last():
            return (self.time - last_launch.time).total_seconds()
        return None

    def get_stage_flights_and_turnaround(self, stage: Stage) -> tuple:
        """Takes in a stage that is on the launch and returns the number of times it's flown (including this launch) and the turnaround time between this launch and last"""
        flights = 0
        time = self.time
        turnaround = turnaround_time(
            Launch.objects.filter(stageandrecovery__stage=stage, time__lte=time).order_by("time")
        )
        if turnaround:
            turnaround = round(turnaround / 86400, 2)
        flights += Launch.objects.filter(stageandrecovery__stage=stage, time__lte=time).count()

        return (flights, turnaround)

    def get_rocket_flights_reused_vehicle(self) -> int:
        """Up to and including the launch, counts number of launches of that vehicle that have flown with one or more flight proven boosters; increments by one regardless of if one, two, or three boosters are flight proven"""
        return (
            Launch.objects.filter(time__lte=self.time, rocket=self.rocket, stageandrecovery__num_flights__gt=1)
            .distinct()
            .count()
        )

    def get_total_reflights(
        self, stage_type: str, start: datetime = datetime(2000, 1, 1, tzinfo=pytz.utc)
    ) -> list[int]:
        """Counts total number of stage reflights past the starting date; so this function increments by two if two stages (both boosters or second stages) are flight proven on Falcon Heavy"""
        num_stage_reflights = (
            StageAndRecovery.objects.filter(
                launch__time__lt=self.time,
                launch__time__gte=start,
                launch__rocket__family=self.rocket.family,
                num_flights__gt=1,
                stage__type=stage_type,
            ).count()
            + 1
        )  # 1 added since lower bound is inclusive

        num_stages_reflown_on_launch = StageAndRecovery.objects.filter(launch=self, num_flights__gt=1).count()

        return list(range(num_stage_reflights, num_stage_reflights + num_stages_reflown_on_launch))

    def get_num_stage_landings(self, stage_type: str) -> list[int]:
        """Returns a list of ints with total number of stage landings on that flight; for example if all three FH cores land: [123, 124, 125]"""
        num_stage_landings = (
            StageAndRecovery.objects.filter(launch__time__lt=self.time, stage__type=stage_type)
            .filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
            .filter(method_success="SUCCESS")
            .count()
        ) + 1

        num_landings_on_launch = (
            StageAndRecovery.objects.filter(launch=self, stage__type=stage_type)
            .filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
            .filter(Q(method_success="SUCCESS") | Q(launch__time__gte=datetime.now(pytz.utc)))
            .count()
        )

        return list(range(num_stage_landings, num_stage_landings + num_landings_on_launch))

    def get_year_launch_num(self) -> int:
        """Returns int for number of launches"""
        return Launch.objects.filter(
            time__gte=datetime(self.time.year, 1, 1, tzinfo=pytz.utc),
            time__lte=self.time,
        ).count()

    def get_launches_from_pad(self) -> int:
        """Returns int for number of launches from pad"""
        return Launch.objects.filter(pad=self.pad, time__lte=self.time).count()

    # Returns list of turnaround times for object type
    def get_queryset(self, turnaround_object: TurnaroundObjects):
        if turnaround_object == TurnaroundObjects.BOOSTER:
            return Stage.objects.filter(type="BOOSTER").distinct()
        if turnaround_object == TurnaroundObjects.SECOND_STAGE:
            return Stage.objects.filter(type="SECOND_STAGE").distinct()
        if turnaround_object == TurnaroundObjects.PAD:
            return Pad.objects.all()
        if turnaround_object == TurnaroundObjects.LANDING_ZONE:
            return LandingZone.objects.all()
        if turnaround_object == TurnaroundObjects.SPACECRAFT:
            return Spacecraft.objects.all()
        if turnaround_object == TurnaroundObjects.ALL:
            return [""]
        return None

    def get_launches(self, item):
        if isinstance(item, Stage):
            return Launch.objects.filter(stageandrecovery__stage=item, time__lte=self.time).order_by("time").all()
        if isinstance(item, Pad):
            return Launch.objects.filter(pad=item, time__lte=self.time).order_by("time").all()
        if isinstance(item, LandingZone):
            return (
                Launch.objects.filter(stageandrecovery__landing_zone=item, time__lte=self.time).order_by("time").all()
            )
        return Launch.objects.filter(time__lte=self.time).order_by("time").all()

    def calculate_turnarounds(self, turnaround_object: TurnaroundObjects) -> dict:
        """
        Takes in an object, returns a list of turnarounds sorted from quickest to longest.
        Return format style: (Bool (is this a new record), [[Object, Int (num of seconds turnaround), launch, last launch],...])
        """
        turnarounds: list = []
        new_record: bool = False
        queryset = self.get_queryset(turnaround_object)

        if queryset is None:
            return None

        for item in queryset:
            launches = self.get_launches(item)

            # Cycle through the launches one at a time to calculate the needed turnaround
            for i in range(0, len(launches) + 1):
                turnaround = turnaround_time(launches=launches[:i])
                if turnaround:
                    turnarounds.append(
                        {
                            "turnaround_object": item,
                            "turnaround_time": turnaround,
                            "launch_name": launches[i - 1].name,
                            "last_launch_name": launches[i - 2].name,
                        }
                    )

        # Sort the turnarounds so they go in order of quickest to slowest (or non-applicable) turnaround
        turnarounds = sorted(
            turnarounds,
            key=lambda x: (
                x["turnaround_time"] is None,
                (x["turnaround_time"] if x["turnaround_time"] is not None else float("inf")),
            ),
        )

        # Record if this launch sets a new quickest turnaround
        if turnarounds and turnarounds[0]["launch_name"] == self.name:
            new_record = True

        if turnarounds:
            return {"is_record": new_record, "ordered_turnarounds": turnarounds}
        return None

    def calculate_stage_and_recovery_turnaround_stats(self, turnaround_object: str, stats: list):
        # Build query filters
        q_objects = Q(
            launch__time__lte=self.time,
            launch__rocket__family=self.rocket.family,
        )

        # Determine order_by and item based on the turnaround_object
        if turnaround_object in ["booster", "second stage"]:
            order_by = "stage_turnaround"
            q_objects &= Q(
                **{"stage__type": turnaround_object.replace(" ", "_").upper(), "stage_turnaround__isnull": False}
            )
            item = f"a {self.rocket.family} {turnaround_object}"
            filter_field = "stage"
            related_model = Stage
        else:
            order_by = "zone_turnaround"
            q_objects &= Q(**{"landing_zone__isnull": False, "zone_turnaround__isnull": False})
            item = f"a {self.rocket.family} recovery zone"
            filter_field = "landing_zone"
            related_model = LandingZone

        # Filter and order the stage and recovery objects
        stage_and_recoveries = StageAndRecovery.objects.filter(q_objects).order_by(order_by)

        # Return None if less than 3 records are found
        if stage_and_recoveries.count() < 3:
            return

        # Prepare the stats if the first record's launch is not the current launch
        if stage_and_recoveries.first().launch != self:
            for related_instance in related_model.objects.filter(stageandrecovery__launch=self):
                filtered_recoveries = stage_and_recoveries.filter(**{filter_field: related_instance})
                if filtered_recoveries.count() < 3 or filtered_recoveries.first().launch != self:
                    continue

                turnaround = getattr(filtered_recoveries.first(), order_by)
                old_turnaround = getattr(filtered_recoveries[1], order_by)

                stats.append(
                    (
                        turnaround_object == "landing zone",
                        f"– Fastest turnaround of {related_instance.name} to date at {convert_seconds(turnaround)}. Previous record: {convert_seconds(old_turnaround)}",
                    )
                )

            return

        # If the first record's launch is the current launch, return the fastest turnaround for the item
        turnaround = getattr(stage_and_recoveries.first(), order_by)
        old_turnaround = getattr(stage_and_recoveries[1], order_by)
        previous_name = (
            stage_and_recoveries[1].stage.name if filter_field == "stage" else stage_and_recoveries[1].landing_zone.name
        )

        stats.append(
            (
                True,
                f"– Fastest turnaround of {item} to date at {convert_seconds(turnaround)}. Previous record: {previous_name} at {convert_seconds(old_turnaround)}",
            )
        )

    def calculate_turnaround_stats(self, turnaround_object: TurnaroundObjects, stats: list):
        # Define common query filters
        q_objects = Q(
            time__lte=self.time,
            rocket__family=self.rocket.family,
        )

        # Set order_by and item based on turnaround_object
        if turnaround_object == TurnaroundObjects.ALL:
            order_by = "company_turnaround"
            item = f"{self.rocket.family.provider}"
        elif turnaround_object == TurnaroundObjects.PAD:
            order_by = "pad_turnaround"
            item = f"a {self.rocket.family.provider} pad"

        # Fetch and order launches based on the criteria
        launches = Launch.objects.filter(q_objects).order_by(order_by)

        # If fewer than 2 launches are found, return None
        if launches.count() < 3:
            return

        # Handle specific case for PAD turnaround
        if turnaround_object == TurnaroundObjects.PAD:
            launches = launches.filter(pad=self.pad)
            if launches.count() < 3 or launches.first() != self:
                return
            item = self.pad.nickname

        # If the first launch isn't the current one, we return early
        if launches.first() != self:
            return

        # Calculate turnaround times
        turnaround = convert_seconds(getattr(launches.first(), order_by))
        old_turnaround = convert_seconds(getattr(launches[1], order_by))

        # Add pad-specific details if applicable
        if turnaround_object == TurnaroundObjects.PAD:
            old_turnaround = f"{launches[1].pad.nickname} at {old_turnaround}"

        stats.append(
            (
                True,
                f"– Fastest turnaround of {item} to date at {turnaround}. Previous record: {old_turnaround}",
            )
        )

    def get_consec_landings(self, stage_type: str) -> list[int]:
        """Returns the number of successful stage landings in a row; in the event of a Falcon Heavy with a booster landing failure, add in order landings occured to ensure this returns correct value"""
        count: int = 0
        count_list: list[str] = []

        # Cycle through all previous launches to check for failures
        for landing in (
            StageAndRecovery.objects.filter(
                launch__time__lt=self.time, stage__type=stage_type, launch__rocket__family=self.rocket.family
            )
            .filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
            .order_by("-launch__time", "-id")
            .all()
        ):
            if landing.method_success == "SUCCESS" or landing.launch.time > datetime.now(pytz.utc):
                count += 1
            else:
                break

        # Cycle through recoveries on launch
        for landing in (
            StageAndRecovery.objects.filter(launch=self, stage__type=stage_type)
            .filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
            .order_by("id")
        ):
            if landing.method_success == "FAILURE":
                count = 0
                count_list = []
            if landing.method_success == "SUCCESS" or self.time > datetime.now(pytz.utc):
                count += 1
                count_list.append(count)
        return count_list

    @property
    def boosters(self) -> str:
        """Returns concatenated string of boosters on launch; these are ordered by position (so center, MY, PY) for three core launches"""
        boosters = []
        for stage in Stage.objects.filter(stageandrecovery__launch=self).order_by("stageandrecovery__stage_position"):
            boosters.append(f"{stage}-{self.get_stage_flights_and_turnaround(stage=stage)[0]}")
        return concatenated_list(boosters).replace("N/A", "Unknown")

    @property
    def recoveries(self) -> str:
        """Returns concatenated string of recoveries on launch; these are ordered by position (so center, MY, PY) for three core launches"""
        recoveries = []
        for stage_and_recovery in StageAndRecovery.objects.filter(launch=self).order_by("stage_position"):
            if stage_and_recovery.landing_zone:
                recoveries.append(f"{stage_and_recovery.landing_zone.nickname}")
            else:
                recoveries.append("Expended")
        return concatenated_list(recoveries)

    def make_booster_display(self) -> str:
        """Returns booster display for launch; returns all boosters on flight (with flight number) and turnaround. Ordered by position of cores"""
        stages_string = ""
        turnaround_string = ""
        stage_known = False

        # Create the strings for stages and turnarounds
        for stage_and_recovery in StageAndRecovery.objects.filter(launch=self).order_by("stage_position"):
            stage_known = stage_and_recovery.stage
            if stage_known:
                stages_string += stage_and_recovery.stage.name + "-" + f"{stage_and_recovery.num_flights}" + ", "

            turnaround_string += (
                f"{round(stage_and_recovery.stage_turnaround / 86400, 2):.2f}"
                if stage_and_recovery.stage_turnaround is not None
                else "N/A"
            )
            turnaround_string += ", "

        # Format string to be readable
        stages_string = stages_string.rstrip(" ").rstrip(",")
        turnaround_string = turnaround_string.rstrip(" ").rstrip(",")
        if stage_known:
            turnaround_string += "-day turnaround"
            return " " + stages_string + "; " + turnaround_string
        return "; Unknown booster"

    # Figure out where stages will land or where they landed; change tense based on portion of time. Accounts for soft ocean landings as well
    def make_landing_string(self) -> str:
        """Returns string of where stage will land or landed; accounts for ocean splashdowns and expended vehicles"""
        # pylint: disable=too-many-branches
        launch_landings = ""

        for item in StageAndRecovery.objects.filter(launch=self).order_by("stage_position"):
            if item.stage:
                name = item.stage.name
            else:
                name = "The booster"
            if self.time > datetime.now(pytz.utc):
                if item.method == "EXPENDED":
                    launch_landings += f"{name} will be expended; "
                elif item.method == "OCEAN_SURFACE":
                    launch_landings += f"{name} will attempt a soft landing on the ocean surface; "
                else:
                    if item.landing_zone:
                        launch_landings += (
                            f"{name} will be recovered on {item.landing_zone.name} ({item.landing_zone.nickname}); "
                        )
            else:
                if item.method == "EXPENDED":
                    launch_landings += f"{name} was expended; "
                elif item.method == "OCEAN_SURFACE":
                    launch_landings += f"{name} {success(item.method_success)} a soft landing on the ocean surface; "
                else:
                    if item.landing_zone:
                        launch_landings += f"{name} {success(item.method_success)} a landing on {item.landing_zone.name} ({item.landing_zone.nickname}); "

        # In the event when there are no stage and recovery objects for the launch (such as the booster is not known) the string is set to expended
        if launch_landings == "":
            if self.time > datetime.now(pytz.utc):
                launch_landings = "The stage will be expended"
            else:
                launch_landings = "The stage was expended"
        launch_landings: list = launch_landings.rstrip("; ")

        return launch_landings

    def get_booster_reuse_stats(self, stats: list):
        if not self.flight_proven_booster:
            return
        booster_reuse = self.get_rocket_flights_reused_vehicle()

        booster_reflights = self.get_total_reflights(stage_type="BOOSTER")
        booster_reflight_string = concatenated_list([make_ordinal(reflight) for reflight in booster_reflights])
        booster_reflights_year = self.get_total_reflights(
            stage_type="BOOSTER", start=datetime(self.time.year - 1, 12, 31, 23, 59, 59, 999, tzinfo=pytz.utc)
        )
        booster_reflight_year_string = concatenated_list(
            [make_ordinal(reflight) for reflight in booster_reflights_year]
        )

        stats.append(
            (
                is_significant(booster_reuse),
                f"– {make_ordinal(booster_reuse)} {self.rocket} flight with a flight-proven booster",
            )
        )
        stats.append(
            (
                is_significant(booster_reflights),
                f"– {booster_reflight_string} reflight of a {self.rocket.family} booster",
            )
        )
        stats.append(
            (
                is_significant(booster_reflights_year),
                f"– {booster_reflight_year_string} reflight of a {self.rocket.family} booster in {self.time.year}",
            )
        )

    def get_booster_landing_stats(self, stats: list):
        booster_landings = self.get_num_stage_landings(stage_type="BOOSTER")
        if booster_landings:
            booster_landing_string = concatenated_list([make_ordinal(landing) for landing in booster_landings])
            consec_booster_landings = self.get_consec_landings(stage_type="BOOSTER")
            consec_booster_landing_string = concatenated_list(
                [make_ordinal(landing) for landing in consec_booster_landings]
            )
            make_plural = "s" if self.num_successful_landings > 1 else ""

            stats.append((is_significant(booster_landings), f"– {booster_landing_string} booster landing{make_plural}"))
            stats.append(
                (
                    is_significant(consec_booster_landings),
                    f"– {consec_booster_landing_string} consecutive {self.rocket.family} booster landing{make_plural}",
                )
            )

    def get_launch_year_stats(self, stats: list):
        year_launch_num = self.get_year_launch_num()
        stats.append(
            (
                is_significant(year_launch_num),
                f"– {make_ordinal(year_launch_num)} {self.rocket.family.provider} launch of {self.time.year}",
            ),
        )

    def get_launch_pad_stats(self, stats: list):
        num_launches_from_pad = self.get_launches_from_pad()
        stats.append(
            (
                is_significant(num_launches_from_pad),
                f"– {make_ordinal(num_launches_from_pad)} {self.rocket.family.provider} launch from {self.pad.nickname}",
            )
        )

    def make_stats(self) -> list:
        """Returns a list of stats for the mission; non-trivial stats not returned"""
        stats: list[tuple] = []

        rocket_launch_num = Launch.objects.filter(rocket=self.rocket, time__lte=self.time).count()
        stats.append(
            (is_significant(rocket_launch_num), f"– {make_ordinal(rocket_launch_num)} {self.rocket.name} mission")
        )

        self.get_booster_reuse_stats(stats)
        self.get_booster_landing_stats(stats)
        self.get_launch_year_stats(stats)
        self.get_launch_pad_stats(stats)

        # Adding turnaround stats
        self.calculate_stage_and_recovery_turnaround_stats(turnaround_object="booster", stats=stats)
        self.calculate_stage_and_recovery_turnaround_stats(turnaround_object="second stage", stats=stats)
        self.calculate_turnaround_stats(turnaround_object=TurnaroundObjects.PAD, stats=stats)
        self.calculate_turnaround_stats(turnaround_object=TurnaroundObjects.ALL, stats=stats)

        for stat in LaunchStat.objects.filter(launch=self):
            stats.append((stat.significant, f"– {stat.string}"))

        return stats

    def make_x_post(self):
        stats = self.make_stats()

        significant_stats = []
        other_stats = []

        def first_lower(string: str):
            if string:
                return string[0].lower() + string[1:]
            return string

        for stat in stats:
            if stat[0]:
                significant_stats.append(first_lower(stat[1].replace("– ", "")))
            else:
                other_stats.append(first_lower(stat[1].replace("– ", "")))

        def get_random_stat(stat_list):
            return stat_list.pop(random.randint(0, len(stat_list) - 1)) if stat_list else None

        stat = get_random_stat(significant_stats) or get_random_stat(other_stats)
        if not stat:
            return None

        additional_stat = get_random_stat(significant_stats) or get_random_stat(other_stats)

        if additional_stat:
            new_stat_string = f"{additional_stat} and {stat}"
            new_post_string = f"{self.name} will mark {self.rocket.family.provider}'s {new_stat_string}./nLearn more: https://boostertracker.com/launch/{self.id}"
            if len(new_post_string) <= 280:
                return new_post_string

        return f"{self.name} will mark {self.rocket.family.provider}'s {stat}./nLearn more: https://boostertracker.com/launch/{self.id}"

    def set_timezone(self):
        if self.pad.nickname == "SLC-4E":
            time_zone = "US/Pacific"
        elif self.pad.nickname in ("SLC-40", "LC-39A"):
            time_zone = "US/Eastern"
        elif self.pad.nickname == "OLP-A":
            time_zone = "US/Central"
        elif self.pad.name == "Omelek Island":
            time_zone = "Etc/GMT+12"
        else:
            time_zone = "UTC"

        return pytz.timezone(time_zone)

    def update_data_with_launch_info(self, data, liftoff_time_local):
        launch_location = f"{self.pad.name} ({self.pad.nickname}), {self.pad.location}"
        boosters_display = self.make_booster_display()
        launch_landings = self.make_landing_string()

        data["Liftoff Time"] = [
            f"{format_time(self.time)}",
            f"{format_time(liftoff_time_local)}",
        ]
        data["Mission Name"] = [self.name]
        data["Customer <br /> (Who's paying for this?)"] = [self.customer]
        data["Rocket"] = [f"{self.rocket}{boosters_display}"]
        data["Launch Location"] = [launch_location]
        if self.mass:
            data["Payload mass"] = [f"{self.mass:,} kg ({int(round(self.mass * 2.2, -2)):,} lb)"]
        else:
            data["Payload mass"] = ["Unknown"]
        data["Where are the satellites going?"] = [self.orbit.name] if self.orbit else ["Unknown"]
        data["Where will the first stage land?"] = [launch_landings]

        if self.droneship_needed:
            data["Where will the first stage land?"].append("")
            data["Where will the first stage land?"].append(
                f"Tug: {concatenated_list(list(set(Boat.objects.filter(tugonlaunch__launch=self).values_list('name', flat=True))))}; Support: {concatenated_list(list(set(Boat.objects.filter(supportonlaunch__launch=self).values_list('name', flat=True))))}"
            )

    def update_data_with_fairing_recovery(self, data):
        if FairingRecovery.objects.filter(launch=self).exists():
            if self.time > datetime.now(pytz.utc):
                data["Will they be attempting to recover the fairings?"].append(
                    f"The fairing halves will be recovered from the water by {concatenated_list(list(set(Boat.objects.filter(fairingrecovery__launch=self).values_list('name', flat=True))))}"
                )
            else:
                data["Will they be attempting to recover the fairings?"].append(
                    f"The fairing halves were recovered by {concatenated_list(list(set(Boat.objects.filter(fairingrecovery__launch=self).values_list('name', flat=True))))}"
                )
        else:
            data["Will they be attempting to recover the fairings?"].append("There are no fairings on this flight")

    def update_data_with_stats(self, data):
        # Have the significant stats appear first
        stats = sorted(self.make_stats(), key=lambda x: x[0], reverse=True)
        stats_only = [stat[1] for stat in stats]
        data["This will be the"] = stats_only

    def create_launch_table(self) -> str:
        """Returns an EDA-style launch table for the launch"""
        # Data contains table titles
        data = {
            "Liftoff Time": [],
            "Mission Name": [],
            "Launch Provider <br /> (What rocket company is launching it?)": ["SpaceX"],
            "Customer <br /> (Who's paying for this?)": [],
            "Rocket": [],
            "Launch Location": [],
            "Payload mass": [],
            "Where are the satellites going?": [],
            "Where will the first stage land?": [],
            "Will they be attempting to recover the fairings?": [],
            "This will be the": [],
        }

        time_zone = self.set_timezone()
        liftoff_time_local = self.time.astimezone(time_zone)
        self.update_data_with_launch_info(data, liftoff_time_local)
        self.update_data_with_fairing_recovery(data)
        self.update_data_with_stats(data)

        # Change title of headings if launch is in the past
        if self.time < datetime.now(pytz.utc):
            post_launch_data = [
                "Liftoff Time",
                "Mission Name",
                "Launch Provider <br /> (What rocket company launched it?)",
                "Customer <br /> (Who paid for this?)",
                "Rocket",
                "Launch Location",
                "Payload mass",
                "Where did the satellites go?",
                "Where did the first stage land?",
                "Did they attempt to recover the fairings?",
                "This was the",
            ]
            ordered_data = {new_key: data.get(old_key, None) for old_key, new_key in zip(data.keys(), post_launch_data)}
            data = ordered_data

        # print(self.build_table_html(data))
        return data


class LaunchStat(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    significant = models.BooleanField()
    string = models.CharField(max_length=400)


class LandingZone(models.Model):
    name = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=20)
    type = models.CharField(max_length=100, choices=RECOVERY_METHODS)
    serial_number = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, choices=LIFE_OPTIONS, default="ACTIVE")
    image = models.ImageField(upload_to="landing_zone_photos/", default="media/pad_photos/default.png")
    credit = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Landing Zones"

    @property
    def num_landings(self) -> int:
        """Returns the number of successful landings on landing zone"""
        return Launch.objects.filter(
            stageandrecovery__landing_zone=self,
            time__lte=datetime.now(pytz.utc),
            stageandrecovery__method_success="SUCCESS",
        ).count()

    @property
    def fastest_turnaround(self):
        """Returns the fastest turnaround of landing zone"""
        if (
            stage_and_recovery := StageAndRecovery.objects.filter(
                launch__time__lte=datetime.now(pytz.utc), landing_zone=self
            )
            .order_by("zone_turnaround")
            .first()
        ):
            if stage_and_recovery is None or stage_and_recovery.zone_turnaround is None:
                return "N/A"
            return convert_seconds(stage_and_recovery.zone_turnaround)

        return "N/A"


class StageAndRecovery(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True, blank=True)
    stage_position = models.CharField(
        max_length=50,
        choices=BOOSTER_TYPES,
        null=True,
        blank=True,
        default="SINGLE_CORE",
    )
    landing_zone = models.ForeignKey(LandingZone, on_delete=models.CASCADE, null=True, blank=True)
    method = models.CharField(max_length=200, choices=RECOVERY_METHODS)
    method_success = models.CharField(max_length=200, choices=LANDING_METHOD_OUTCOMES, null=True, blank=True)
    recovery_success = models.BooleanField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    id = models.AutoField(primary_key=True)
    stage_turnaround = models.IntegerField(blank=True, null=True, editable=False)
    zone_turnaround = models.IntegerField(blank=True, null=True, editable=False)
    num_flights = models.IntegerField(blank=True, null=True, editable=False)
    num_recoveries = models.IntegerField(blank=True, null=True, editable=False)

    def __str__(self):
        if self.stage and self.stage.name:
            return f"{self.stage.name} recovery"
        return "Unknown recovery"

    _from_task = False

    class Meta:
        constraints = [models.UniqueConstraint(fields=["launch", "stage"], name="unique_launch_stage")]

        verbose_name_plural = "Stage Recoveries"

    @property
    def get_stage_turnaround(self):
        if (
            last_launch := StageAndRecovery.objects.filter(stage=self.stage, launch__time__lt=self.launch.time)
            .order_by("launch__time")
            .last()
        ):
            return (self.launch.time - last_launch.launch.time).total_seconds()

        return None

    @property
    def get_zone_turnaround(self):
        if (
            last_launch := StageAndRecovery.objects.filter(
                landing_zone=self.landing_zone, launch__time__lt=self.launch.time
            )
            .order_by("launch__time")
            .last()
        ):
            return (self.launch.time - last_launch.launch.time).total_seconds()

        return None

    @property
    def get_num_flights(self):
        return StageAndRecovery.objects.filter(stage=self.stage, launch__time__lte=self.launch.time).count()

    @property
    def get_num_landings(self):
        return (
            StageAndRecovery.objects.filter(
                landing_zone=self.landing_zone,
                launch__time__lte=self.launch.time,
                method__in=["GROUND_PAD", "DRONE_SHIP", "CATCH"],
            )
            .filter(Q(method_success="SUCCESS") | Q(launch__time__gte=datetime.now(pytz.utc)))
            .count()
        )


class FairingRecovery(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(
        Boat,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "FAIRING_RECOVERY"},
        null=True,
        blank=True,
    )
    catch = models.BooleanField()
    recovery_attempt = models.BooleanField()
    recovery = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    flights = models.IntegerField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Fairing Recoveries"

    def __str__(self):
        if self.boat:
            return f"Fairing recovery with {self.boat.name}"
        return "Unknown fairing recovery"


class TugOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "TUG"})

    class Meta:
        verbose_name_plural = "Tugs on Launch"
        constraints = [models.UniqueConstraint(fields=["launch", "boat"], name="unique_launch_tug")]

    def __str__(self):
        if self.boat:
            return self.boat.name
        return "Tug"


class SupportOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "SUPPORT"})

    class Meta:
        verbose_name_plural = "Support Ships on Launch"
        constraints = [models.UniqueConstraint(fields=["launch", "boat"], name="unique_launch_support")]

    def __str__(self):
        if self.boat:
            return self.boat.name
        return "Boat"


class SpacecraftOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    splashdown_time = models.DateTimeField("Splashdown Time", null=True, blank=True)
    recovery_boat = models.ForeignKey(
        Boat,
        on_delete=models.CASCADE,
        limit_choices_to={"type": "SPACECRAFT_RECOVERY"},
        blank=True,
        null=True,
    )
    spacecraft_turnaround = models.IntegerField(blank=True, null=True, editable=False)
    num_flights = models.IntegerField(blank=True, null=True, editable=False)

    class Meta:
        verbose_name_plural = "Dragon on Launch"
        constraints = [models.UniqueConstraint(fields=["launch", "spacecraft"], name="unique_launch_spacecraft")]

    def __str__(self):
        if self.spacecraft:
            return f"{self.spacecraft.name} on launch"
        return "Spacecraft"

    _from_task = False

    def get_turnaround(self):
        if (
            last_launch := SpacecraftOnLaunch.objects.filter(
                spacecraft=self.spacecraft, launch__time__lt=self.launch.time
            )
            .order_by("splashdown_time")
            .last()
        ):
            return (self.launch.time - last_launch.splashdown_time).total_seconds()

        return None

    def get_num_flights(self):
        return SpacecraftOnLaunch.objects.filter(spacecraft=self.spacecraft, launch__time__lte=self.launch.time).count()


class PadUsed(models.Model):
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="rocket_pad_photos/",
        default="media/pad_photos/default.png",
    )
    credit = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Pads Used"
        constraints = [models.UniqueConstraint(fields=["rocket", "pad"], name="unique_rocket_pad")]

    def __str__(self):
        if self.pad:
            return f"{self.pad.name}"
        return "Pad"
