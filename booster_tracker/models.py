from django.db import models
from booster_tracker.utils import (
    make_ordinal,
    concatenated_list,
    TurnaroundObjects,
    success,
    convert_seconds,
    format_time,
    is_significant,
    get_random_stat,
    process_stat,
)
from datetime import datetime
from django.db.models import Q
from colorfield.fields import ColorField
import pytz
from timezone_field import TimeZoneField

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
    ("TBD", "TBD"),
]
LANDING_METHOD_OUTCOMES = [("SUCCESS", "success"), ("FAILURE", "failure"), ("PRECLUDED", "precluded"), ("TBD", "TBD")]
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
    image = models.ImageField(upload_to="operator_photos/", default="stage_photos/default_booster.jpg")
    credit = models.CharField(max_length=100, blank=True, null=True)

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
    image = models.ImageField(upload_to="rocket_photos/", default="stage_photos/default_booster.jpg")
    credit = models.CharField(max_length=100, null=True, blank=True)
    color = ColorField(default="#218243")

    def __str__(self):
        return self.name

    @property
    def num_launches(self) -> int:
        """Returns number of times rocket has launched up to current time as an int; excludes precluded launches"""
        return Launch.objects.filter(rocket=self, time__lte=datetime.now(pytz.utc), launch_precluded=False).count()

    @property
    def num_successes(self) -> int:
        """Returns number of times rocket has launched successfully up to current time as an int"""
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
    def num_launches(self) -> int:
        """Returns number of times a stage has flown up to current time as an int"""
        return StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc), stage=self).count()

    @property
    def fastest_turnaround(self) -> int:
        """Returns the fastest turnaround of the stage to date; returns turnaround in total seconds"""
        if (
            stageandrecovery := StageAndRecovery.objects.filter(stage=self, launch__time__lte=datetime.now(pytz.utc))
            .order_by("stage_turnaround")
            .first()
        ):
            return stageandrecovery.stage_turnaround
        return None


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
    def num_launches(self) -> int:
        """Returns number of times a spacecraft has flown up to current time as an int"""
        return SpacecraftOnLaunch.objects.filter(launch__time__lte=datetime.now(pytz.utc), spacecraft=self).count()

    @property
    def fastest_turnaround(self) -> int:
        """Returns the fastest turnaround of the spacecraft to date; returns turnaround in total seconds"""
        if (
            spacecraftonlaunch := SpacecraftOnLaunch.objects.filter(
                launch__time__lte=datetime.now(pytz.utc), spacecraft=self
            )
            .order_by("spacecraft_turnaround")
            .first()
        ):
            return spacecraftonlaunch.spacecraft_turnaround
        return None


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
    time_zone = TimeZoneField(use_pytz=True, choices_display="WITH_GMT_OFFSET")
    status = models.CharField(max_length=20, choices=LIFE_OPTIONS, default="ACTIVE")
    image = models.ImageField(upload_to="pad_photos/", default="media/pad_photos/default.png")
    credit = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.nickname

    @property
    def num_launches(self) -> int:
        """Returns number of launches from a pad up to current time as an int"""
        return Launch.objects.filter(pad=self, time__lte=datetime.now(pytz.utc), launch_precluded=False).count()

    @property
    def fastest_turnaround(self) -> int:
        """Returns the fastest turnaround of the stage to date; returns turnaround in total seconds"""
        if (
            launch := Launch.objects.filter(pad=self, time__lte=datetime.now(pytz.utc))
            .order_by("pad_turnaround")
            .first()
        ):
            return launch.pad_turnaround
        return None


class Launch(models.Model):
    time = models.DateTimeField("Launch Time")
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    orbit = models.ForeignKey(Orbit, on_delete=models.CASCADE, null=True, blank=True)
    mass = models.IntegerField(blank=True, null=True, verbose_name="Mass (kg)")
    customer = models.CharField(max_length=200)
    launch_outcome = models.CharField(max_length=200, choices=LAUNCH_OUTCOMES, default="TBD")
    exclude_from_missions = models.BooleanField(
        default=False, help_text="Exclude from mission number (Ex: Starship test missions)"
    )
    launch_precluded = models.BooleanField(default=False, help_text="Exclude from launch number (Ex: AMOS-6)")
    pad_turnaround = models.IntegerField(blank=True, null=True, editable=False)
    company_turnaround = models.IntegerField(blank=True, null=True, editable=False)
    image = models.CharField(max_length=200, blank=True, null=True, editable=False)
    stages_string = models.CharField(max_length=500, blank=True, null=True, editable=False)
    celery_task_id = models.CharField(max_length=255, null=True, blank=True, editable=False)
    x_post_sent = models.BooleanField(default=False, editable=False)

    class Meta:
        verbose_name_plural = "Launches"
        ordering = ["-time"]

    def __str__(self):
        return self.name

    # Values to ensure infinite loop is not created from signals file
    _from_task = False
    _is_updating_scheduled_post = False

    @property
    def get_image(self) -> str:
        """Returns the image url stored in database"""
        return PadUsed.objects.get(pad=self.pad, rocket=self.rocket).image.url

    @property
    def droneship_needed(self) -> bool:
        """Returns bool of if a droneship was needed/used on launch"""
        return StageAndRecovery.objects.filter(launch=self, method="DRONE_SHIP").exists()

    @property
    def flight_proven_stage(self) -> bool:
        """Returns bool of if any stage on the launch was flight proven"""
        return StageAndRecovery.objects.filter(launch=self, num_flights__gt=1).exists()

    @property
    def get_company_turnaround(self) -> int:
        """Returns the time between this launch and the last launch from the launch provider in total second int format"""
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
    def get_pad_turnaround(self) -> int:
        """Returns the time between this launch and last launch from pad in total second int format"""
        if last_launch := Launch.objects.filter(pad=self.pad, time__lt=self.time).order_by("time").last():
            return (self.time - last_launch.time).total_seconds()
        return None

    def get_stage_flights(self, stage: Stage) -> int:
        """Given a stage on the launch, returns its turnaround in total seconds from last launch (int)"""
        return Launch.objects.filter(stageandrecovery__stage=stage, time__lte=self.time).count()

    def calculate_stage_and_recovery_turnaround_stats(self, turnaround_object: str) -> list[tuple]:
        """Returns stats for fastest stage/landing zone turnaround; list contains tuples of following format: (bool, str); bool is if the stat is significant, str the stat"""
        # Common filter items
        q_objects = Q(
            launch__time__lte=self.time,
            launch__rocket__family=self.rocket.family,
        )

        stats = []

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

        # Return empty list if less than 3 records are found
        if stage_and_recoveries.count() < 3:
            return stats

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
                        True,
                        f"Fastest turnaround of {related_instance.name} to date at {convert_seconds(turnaround)}. Previous record: {convert_seconds(old_turnaround)}",
                    )
                )

            return stats

        # If the first record's launch is the current launch, return the fastest turnaround for the item
        turnaround = getattr(stage_and_recoveries.first(), order_by)
        old_turnaround = getattr(stage_and_recoveries[1], order_by)
        previous_name = (
            stage_and_recoveries[1].stage.name if filter_field == "stage" else stage_and_recoveries[1].landing_zone.name
        )

        stats.append(
            (
                True,
                f"Fastest turnaround of {item} to date at {convert_seconds(turnaround)}. Previous record: {previous_name} at {convert_seconds(old_turnaround)}",
            )
        )

        return stats

    def calculate_company_turnaround_stats(self) -> list[tuple]:
        """Returns stats for fastest company turnaround; list contains tuples of following format: (bool, str); bool is if the stat is significant, str the stat"""
        launches = Launch.objects.filter(
            time__lte=self.time, rocket__family__provider=self.rocket.family.provider
        ).order_by("company_turnaround")

        if launches.count() < 3 or launches.first() != self:
            return []

        return [
            (
                True,
                f"Shortest time between two {self.rocket.family.provider} launches to date at {convert_seconds(launches[0].company_turnaround)}. Previous record: {convert_seconds(launches[1].company_turnaround)}",
            )
        ]

    def calculate_pad_turnaround_stats(self) -> list[tuple]:
        """Returns stats for fastest pad turnaround; list contains tuples of following format: (bool, str); bool is if the stat is significant, str the stat"""
        # Fetch and order launches based on the criteria
        launches = Launch.objects.filter(
            time__lte=self.time, rocket__family__provider=self.rocket.family.provider
        ).order_by("pad_turnaround")

        # If fewer than 3 launches are found, return empty list
        if launches.count() < 3:
            return []

        if launches.first() == self:
            # Calculate turnaround times
            turnaround = convert_seconds(launches[0].pad_turnaround)
            old_turnaround = convert_seconds(launches[1].pad_turnaround)

            return [
                (
                    True,
                    f"Fastest turnaround of a {self.rocket.family.provider} pad to date at {turnaround}. Previous record: {launches[1].pad.nickname} at {old_turnaround}",
                )
            ]

        # Filter down to launches from pad for pad-specific record
        launches = launches.filter(pad=self.pad)
        if launches.count() < 3 or launches.first() != self:
            return []

        # Calculate turnaround times
        turnaround = convert_seconds(launches[0].pad_turnaround)
        old_turnaround = convert_seconds(launches[1].pad_turnaround)

        return [
            (
                True,
                f"Fastest turnaround of {self.pad.nickname} to date at {turnaround}. Previous record: {old_turnaround}",
            )
        ]

    @property
    def stages(self) -> str:
        """Returns concatenated string of stages on launch; these are ordered by position (so center, MY, PY) for three core launches"""
        stages = []
        for stage in Stage.objects.filter(stageandrecovery__launch=self).order_by("stageandrecovery__stage_position"):
            stages.append(f"{stage}-{self.get_stage_flights(stage=stage)}")
        return concatenated_list(stages).replace("N/A", "Unknown")

    def make_stage_display(self) -> str:
        """Returns stage display for launch; returns all stages on flight (with flight number) and turnaround. Ordered by position of cores"""
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
        stages_string = stages_string.rstrip(", ")
        turnaround_string = turnaround_string.rstrip(", ")
        if stage_known:
            turnaround_string += "-day turnaround"
            return " " + stages_string + "; " + turnaround_string
        return "; Unknown booster"

    def make_landing_string(self) -> str:
        """Returns string of where stage will land or landed; accounts for ocean splashdowns and expended vehicles"""
        # pylint: disable=too-many-branches
        launch_landings = ""

        for item in StageAndRecovery.objects.filter(launch=self).order_by("stage_position"):
            name = item.stage.name if item.stage else "The booster"

            if self.time > datetime.now(pytz.utc):
                if item.method == "EXPENDED":
                    launch_landings += f"{name} will be expended; "
                elif item.method == "OCEAN_SURFACE":
                    launch_landings += f"{name} will attempt a soft landing on the ocean surface; "
                elif item.landing_zone:
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

    def make_stats(self, return_significant_only: bool = True) -> list:
        """Returns a list of stats for the mission; trivial stats not returned"""
        stats: list[tuple] = []

        stats += self.get_rocket_stats()
        stats += self.get_launch_pad_stats()
        stats += self.get_launch_provider_stats()

        for stage_and_recovery in StageAndRecovery.objects.filter(launch=self).order_by("id"):
            stats += stage_and_recovery.get_stage_stats()
            stats += stage_and_recovery.get_landing_zone_stats()

        # Adding turnaround stats
        stats += self.calculate_stage_and_recovery_turnaround_stats(turnaround_object="booster")
        stats += self.calculate_stage_and_recovery_turnaround_stats(turnaround_object="second stage")
        stats += self.calculate_stage_and_recovery_turnaround_stats(turnaround_object="landing_zone")
        stats += self.calculate_pad_turnaround_stats()
        stats += self.calculate_company_turnaround_stats()

        for stat in LaunchStat.objects.filter(launch=self):
            stats.append((stat.significant, f"{stat.string}"))

        if return_significant_only:
            return [stat[1] for stat in stats if stat[0]]

        return stats[:10]  # Only return first 10 elements for looks

    def make_stats_for_post(self):
        stats: list[tuple] = []

        stats += self.get_rocket_stats()
        stats += self.get_launch_pad_stats()
        stats += self.get_launch_provider_stats()

        for stage_and_recovery in StageAndRecovery.objects.filter(launch=self):
            stats += stage_and_recovery.get_stage_stats()
            stats += stage_and_recovery.get_landing_zone_stats()

        # Adding turnaround stats
        stats += self.calculate_stage_and_recovery_turnaround_stats(turnaround_object="booster")
        stats += self.calculate_stage_and_recovery_turnaround_stats(turnaround_object="second stage")
        stats += self.calculate_stage_and_recovery_turnaround_stats(turnaround_object="landing_zone")
        stats += self.calculate_pad_turnaround_stats()
        stats += self.calculate_company_turnaround_stats()

        for stat in LaunchStat.objects.filter(launch=self):
            stats.append((stat.significant, f"{stat.string}"))

        # Split each stat's string at the first period and keep only the part before it
        stats = [(stat[0], stat[1].split(".")[0]) for stat in stats]

        return stats

    def make_x_post(self) -> str:
        """Generates a post about the launch (str), including significant and other stats."""
        stats = self.make_stats_for_post()
        significant_stats = []
        other_stats = []

        provider_name = self.rocket.family.provider

        # Separate significant and other stats, and process them
        for stat in stats:
            processed_stat = process_stat(stat[1], provider_name)
            if stat[0]:
                significant_stats.append(processed_stat)
            else:
                other_stats.append(processed_stat)

        # Get a random stat, prefer significant, then fallback to other
        stat = get_random_stat(significant_stats) or get_random_stat(other_stats)
        if not stat:
            return None

        additional_stat = get_random_stat(significant_stats) or get_random_stat(other_stats)

        # Formulate the final post string
        if additional_stat:
            new_stat_string = f"{additional_stat} and {stat}"
            new_post_string = f"{self.name} will mark {provider_name}'s {new_stat_string}.\n\nLearn more: https://boostertracker.com/launch/{self.id}"
            if len(new_post_string) <= 280:
                return new_post_string

        return f"{self.name} will mark {provider_name}'s {stat}.\n\nLearn more: https://boostertracker.com/launch/{self.id}"

    def update_data_with_launch_info(self, data, liftoff_time_local):
        launch_location = f"{self.pad.name} ({self.pad.nickname}), {self.pad.location}"
        boosters_display = self.make_stage_display()
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
        stats = sorted(self.make_stats(return_significant_only=False), key=lambda x: x[0], reverse=True)
        stats_only = [f"– {stat[1]}" for stat in stats]
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

        time_zone = self.pad.time_zone
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

    def get_rocket_stats(self) -> list[tuple]:
        """
        Returns a list of rocket stats for the launch.
        Each tuple contains:
            - A boolean indicating if the stat is significant.
            - A string description of the stat.
        """
        # Define common query parameters
        base_filters = {"time__lte": self.time, "rocket": self.rocket, "launch_precluded": False}

        # Get the number of launches up to this launch
        launch_num = Launch.objects.filter(**base_filters).count()

        # Get the number of launches for the current year
        year_start = datetime(self.time.year, 1, 1, 0, 0, tzinfo=pytz.utc)
        year_launch_num = Launch.objects.filter(time__gte=year_start, **base_filters).count()

        # Get the number of launches with the same outcome
        outcome_num = Launch.objects.filter(
            time__lte=self.time, rocket=self.rocket, launch_outcome=self.launch_outcome
        ).count()

        # Get the number of launches with a flight-proven stage
        flight_proven_stage_num = (
            Launch.objects.filter(stageandrecovery__num_flights__gt=1, **base_filters).distinct().count()
        )

        # Compile stats
        stats = []

        if not self.launch_precluded:
            stats.append((is_significant(launch_num), f"{make_ordinal(launch_num)} {self.rocket} launch"))
            stats.append(
                (
                    is_significant(year_launch_num),
                    f"{make_ordinal(year_launch_num)} {self.rocket} launch in {self.time.year}",
                )
            )

        if self.launch_outcome != "TBD":
            stats.append(
                (
                    is_significant(outcome_num),
                    f"{make_ordinal(outcome_num)} {self.rocket} launch {self.launch_outcome.lower()}",
                )
            )

        if self.flight_proven_stage:
            stats.append(
                (
                    is_significant(flight_proven_stage_num),
                    f"{make_ordinal(flight_proven_stage_num)} {self.rocket} launch with a flight-proven stage",
                )
            )

        return stats

    def get_launch_provider_stats(self) -> list[tuple]:
        """
        Returns a list of stats for the launch provider.
        Each tuple contains:
            - A boolean indicating if the stat is significant.
            - A string description of the stat.
        """
        provider = self.rocket.family.provider
        base_filters = {"rocket__family__provider": provider, "time__lte": self.time}

        # Get the total mission count (excluding missions marked as such)
        mission_num = Launch.objects.filter(exclude_from_missions=False, **base_filters).count()

        # Get the total launch count (excluding precluded launches)
        launch_num = Launch.objects.filter(launch_precluded=False, **base_filters).count()

        # Get the number of launches for the current year
        year_start = datetime(self.time.year, 1, 1, 0, 0, tzinfo=pytz.utc)
        launch_num_year = Launch.objects.filter(time__gte=year_start, launch_precluded=False, **base_filters).count()

        # Get the number of missions with the same outcome
        mission_outcome_num = Launch.objects.filter(
            launch_outcome=self.launch_outcome, exclude_from_missions=False, **base_filters
        ).count()

        stats = []

        # Add mission-related stats (if not excluded from missions)
        if not self.exclude_from_missions:
            stats.append((is_significant(mission_num), f"{make_ordinal(mission_num)} {provider} mission"))

        # Add mission outcome stats
        if self.launch_outcome != "TBD" and not self.exclude_from_missions:
            stats.append(
                (
                    is_significant(mission_outcome_num),
                    f"{make_ordinal(mission_outcome_num)} {provider} mission {self.launch_outcome.lower().replace('_', ' ')}",
                )
            )

        # Add launch-related stats (if not precluded)
        if not self.launch_precluded:
            stats.append((is_significant(launch_num), f"{make_ordinal(launch_num)} {provider} launch"))
            stats.append(
                (
                    is_significant(launch_num_year),
                    f"{make_ordinal(launch_num_year)} {provider} launch of {self.time.year}",
                )
            )

        return stats

    def get_launch_pad_stats(self) -> list[tuple]:
        """
        Returns a list of stats for launches from the current pad.
        Each tuple contains:
            - A boolean indicating if the stat is significant.
            - A string description of the stat.
        """
        provider = self.rocket.family.provider
        num_launches_from_pad = Launch.objects.filter(
            time__lte=self.time, pad=self.pad, rocket__family__provider=provider, launch_precluded=False
        ).count()

        stats = []
        stats.append(
            (
                is_significant(num_launches_from_pad),
                f"{make_ordinal(num_launches_from_pad)} {provider} launch from {self.pad.nickname}",
            )
        )

        return stats


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
    def fastest_turnaround(self) -> int:
        """Returns the fastest turnaround of landing zone in total seconds (int)"""
        if (
            stageandrecovery := StageAndRecovery.objects.filter(
                landing_zone=self, launch__time__lte=datetime.now(pytz.utc)
            )
            .order_by("zone_turnaround")
            .first()
        ):
            return stageandrecovery.zone_turnaround
        return None


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
    method_success = models.CharField(max_length=200, choices=LANDING_METHOD_OUTCOMES, default="TBD")
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

    # Ensure infinite loops are not created when saving tasks
    _from_task = False

    class Meta:
        constraints = [models.UniqueConstraint(fields=["launch", "stage"], name="unique_launch_stage")]
        ordering = ["id"]
        verbose_name_plural = "Stage Recoveries"

    @property
    def get_num_flights(self) -> int:
        """Returns int representing number of flights of the first stage on the launch"""
        return StageAndRecovery.objects.filter(stage=self.stage, launch__time__lte=self.launch.time).count()

    @property
    def get_num_landings(self) -> int:
        """Returns int representing number of landings the recovery zone has"""
        if self.landing_zone:
            return (
                StageAndRecovery.objects.filter(
                    landing_zone=self.landing_zone,
                    launch__time__lte=self.launch.time,
                    method__in=["GROUND_PAD", "DRONE_SHIP", "CATCH"],
                )
                .filter(Q(method_success="SUCCESS") | Q(launch__time__gte=datetime.now(pytz.utc)))
                .count()
            )
        return None

    @property
    def get_stage_turnaround(self) -> int:
        """Returns int representing number of seconds between launch and last launch of booster"""
        if (
            last_launch := StageAndRecovery.objects.filter(stage=self.stage, launch__time__lt=self.launch.time)
            .order_by("launch__time")
            .last()
        ):
            return (self.launch.time - last_launch.launch.time).total_seconds()

        return None

    @property
    def get_zone_turnaround(self) -> int:
        """Returns int representing number of seconds between landing and last landing on zone"""
        if self.landing_zone and (
            last_launch := StageAndRecovery.objects.filter(
                landing_zone=self.landing_zone, launch__time__lt=self.launch.time
            )
            .order_by("launch__time")
            .last()
        ):
            return (self.launch.time - last_launch.launch.time).total_seconds()

        return None

    def get_stage_stats(self) -> list[tuple]:
        """
        Returns a list of stats for the stages.
        Each tuple contains:
            - A boolean indicating if the stat is significant.
            - A string description of the stat.
        """
        if not self.stage:
            return []
        stage_type = self.stage.type if self.stage else "BOOSTER"
        rocket_family = self.launch.rocket.family
        method_outcome = self.method_success if not self.method_success == "TBD" else "SUCCESS"
        now = datetime.now(pytz.utc)

        related_methods = [self.method]

        if self.method == "EXPENDED":
            related_methods.append("OCEAN_SURFACE")

        # Filter for relevant stage and recovery events before this launch
        relevant_stage_and_recoveries = StageAndRecovery.objects.filter(
            stage__type=stage_type,
            launch__rocket__family=rocket_family,
            launch__time__lt=self.launch.time,
            method__in=["DRONE_SHIP", "GROUND_PAD", "CATCH"],
        )

        # Get the number of landing attempts/successes before this launch
        # launches whose method_success is null have outcome not entered; assume success until entered
        landing_attempts_before_launch = relevant_stage_and_recoveries.exclude(method_success="PRECLUDED").count()
        landing_outcome_before_launch = relevant_stage_and_recoveries.filter(method_success=method_outcome).count()

        # Get the number of landing attempts/successes on this launch
        landing_attempt_on_launch = (
            landing_attempts_before_launch
            + StageAndRecovery.objects.filter(launch=self.launch, id__lte=self.id)
            .exclude(method_success="PRECLUDED")
            .count()
        )

        landing_outcome_on_launch = (
            landing_outcome_before_launch
            + StageAndRecovery.objects.filter(launch=self.launch, id__lte=self.id)
            .filter(Q(method_success=method_outcome) | Q(launch__time__gte=now))
            .count()
        )

        num_expended_launches = (
            StageAndRecovery.objects.filter(
                stage__type=stage_type,
                launch__rocket__family=rocket_family,
                launch__time__lt=self.launch.time,
                method__in=["OCEAN_SURFACE", "EXPENDED"],
            )
            .exclude(method_success="PRECLUDED")
            .count()
        )

        # Calculate consecutive successful landings
        consec_count = 0

        # Get total number of consec landings before launch
        for landing in (
            StageAndRecovery.objects.filter(
                launch__time__lt=self.launch.time,
                stage__type=stage_type,
                launch__rocket__family=rocket_family,
            )
            .filter(Q(method__in=["DRONE_SHIP", "GROUND_PAD", "CATCH"]))
            .order_by("-launch__time", "-id")
        ):
            if landing.method_success in ["SUCCESS", "TBD"]:
                consec_count += 1
            else:
                break

        # Cycle through landings on launch
        for landing in (
            StageAndRecovery.objects.filter(
                launch=self.launch,
                stage__type=stage_type,
                id__lte=self.id,
            )
            .filter(Q(method__in=["DRONE_SHIP", "GROUND_PAD", "CATCH"]))
            .order_by("-id")
        ):
            if landing.method_success in ["SUCCESS", "TBD"]:
                consec_count += 1
            else:
                consec_count = 0

        # Get the number of landings with the same method and outcome before the launch
        landing_outcome_and_method_before_launch = StageAndRecovery.objects.filter(
            stage__type=stage_type,
            launch__rocket__family=rocket_family,
            launch__time__lt=self.launch.time,
            method__in=related_methods,
            method_success=method_outcome,
        ).count()

        landing_outcome_and_method_count = (
            landing_outcome_and_method_before_launch
            + StageAndRecovery.objects.filter(
                launch=self.launch,
                id__lte=self.id,
                method__in=related_methods,
                stage__type=stage_type,
            )
            .filter(Q(method_success=method_outcome) | Q(launch__time__gte=now))
            .count()
        )

        # Total stage reflights in family
        reflights_before_launch = StageAndRecovery.objects.filter(
            launch__time__lt=self.launch.time, launch__rocket__family=rocket_family, num_flights__gt=1
        )
        reflight_num_before_launch = reflights_before_launch.count()
        reflight_num_before_launch_in_year = reflights_before_launch.filter(
            launch__time__gte=datetime(self.launch.time.year, 1, 1, tzinfo=pytz.utc)
        ).count()

        reflights_in_family = (
            reflight_num_before_launch
            + StageAndRecovery.objects.filter(launch=self.launch, id__lte=self.id, num_flights__gt=1).count()
        )

        reflights_in_family_year = (
            reflight_num_before_launch_in_year
            + StageAndRecovery.objects.filter(launch=self.launch, id__lte=self.id, num_flights__gt=1).count()
        )

        # Build the landing string
        if self.method in ["DRONE_SHIP", "GROUND_PAD", "CATCH"]:
            landing_string = f"{rocket_family} {stage_type.lower().replace('_', ' ')} landing {method_outcome.lower()} on a {self.method.lower().replace('_', ' ')}"
        elif self.method == "EXPENDED":
            landing_string = f"expended {rocket_family} {stage_type.lower().replace('_', ' ')}"
        elif self.method == "PARACHUTE":
            landing_string = (
                f"{rocket_family} {stage_type.lower().replace('_', ' ')} parachute recovery {method_outcome.lower()}"
            )
        elif self.method == "OCEAN_SURFACE":
            landing_string = (
                f"{rocket_family} {stage_type.lower().replace('_', ' ')} soft ocean splashdown {method_outcome.lower()}"
            )

        # Generate stats list
        stats = []
        if self.launch.time > now or self.method_success != "TBD":
            if not (self.method == "EXPENDED" and self.launch.launch_outcome == "FAILURE"):
                stats.append(
                    (
                        is_significant(landing_outcome_and_method_count),
                        f"{make_ordinal(landing_outcome_and_method_count)} {landing_string}",
                    )
                )

        if self.method == "OCEAN_SURFACE":
            stats.append(
                (
                    is_significant(num_expended_launches),
                    f"{make_ordinal(num_expended_launches)} expended {rocket_family} {stage_type.lower().replace('_', ' ')}",
                )
            )

        if self.method in ["CATCH", "GROUND_PAD", "DRONE_SHIP"]:
            stats.append(
                (
                    is_significant(landing_attempt_on_launch),
                    f"{make_ordinal(landing_attempt_on_launch)} landing attempt of a {rocket_family} {stage_type.lower().replace('_', '' '')}",
                )
            )

            if self.method_success != "TBD" or self.launch.time > now:
                stats.append(
                    (
                        is_significant(landing_outcome_on_launch),
                        f"{make_ordinal(landing_outcome_on_launch)} landing {method_outcome.lower()} of a {rocket_family} {stage_type.lower().replace('_', '' '')}",
                    )
                )

        if method_outcome == "SUCCESS" and self.method in [
            "GROUND_PAD",
            "CATCH",
            "DRONE_SHIP",
        ]:
            if self.method_success != "TBD" or self.launch.time > now:
                stats.append(
                    (
                        is_significant(consec_count),
                        f"{make_ordinal(consec_count)} consecutive landing of a {rocket_family} {stage_type.lower().replace('_', '' '')}",
                    )
                )

        if self.num_flights and self.num_flights > 1:
            stats.append(
                (
                    is_significant(reflights_in_family),
                    f"{make_ordinal(reflights_in_family)} reflight of a {rocket_family} {stage_type.lower().replace('_', '' '')}",
                )
            )
            stats.append(
                (
                    is_significant(reflights_in_family_year),
                    f"{make_ordinal(reflights_in_family_year)} reflight of a {rocket_family} {stage_type.lower().replace('_', '' '')} in {self.launch.time.year}",
                )
            )

        return stats

    def get_landing_zone_stats(self) -> list[tuple]:
        """
        Returns a list of stats for the landing zone.
        Each tuple contains:
            - A boolean indicating if the stat is significant.
            - A string description of the stat.
        """
        # Exit early if no landing zone is specified
        if not self.landing_zone:
            return []

        # Determine the method outcome; default to "SUCCESS" if method outcome is not provided
        method_outcome = self.method_success if self.method_success != "TBD" else "SUCCESS"
        now = datetime.now(pytz.utc)

        # Get the number of landing attempts and successes on the landing zone
        attempts_on_zone = (
            StageAndRecovery.objects.filter(launch__time__lte=self.launch.time, landing_zone=self.landing_zone)
            .exclude(method_success="PRECLUDED")
            .count()
        )

        landings_on_zone = (
            StageAndRecovery.objects.filter(launch__time__lte=self.launch.time, landing_zone=self.landing_zone)
            .filter(Q(method_success=method_outcome) | Q(launch__time__gt=now))
            .count()
        )

        # Generate the stats list
        stats = [
            (
                is_significant(landings_on_zone),
                f"{make_ordinal(landings_on_zone)} landing {method_outcome.lower().replace('_', ' ')} on {self.landing_zone}",
            )
        ]

        # Include landing attempts if the method was not precluded
        if self.method_success != "PRECLUDED":
            stats.append(
                (
                    is_significant(attempts_on_zone),
                    f"{make_ordinal(attempts_on_zone)} landing attempt on {self.landing_zone}",
                )
            )

        return stats


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

    # Ensure infinite loops are not created when saving objects in signal file
    _from_task = False

    def get_num_flights(self) -> int:
        """Returns int representing number of times the spacecraft has flown"""
        return SpacecraftOnLaunch.objects.filter(spacecraft=self.spacecraft, launch__time__lte=self.launch.time).count()

    def get_turnaround(self) -> int:
        """Returns int representing total seconds between splashdown and launch"""
        if (
            last_launch := SpacecraftOnLaunch.objects.filter(
                spacecraft=self.spacecraft, launch__time__lt=self.launch.time
            )
            .order_by("splashdown_time")
            .last()
        ):
            return (self.launch.time - last_launch.splashdown_time).total_seconds()

        return None

    def get_spacecraft_stats(self) -> list[tuple]:
        """
        Returns a list of stats for the spacecraft
        Each tuple contains:
            - A boolean indicating if the stat is significant.
            - A string description of the stat.
        """
        family_launch_num = SpacecraftOnLaunch.objects.filter(
            launch__time__lte=self.launch.time, spacecraft__family=self.spacecraft.family
        ).count()
        family_version_launch_num = SpacecraftOnLaunch.objects.filter(
            launch__time__lte=self.launch.time,
            spacecraft__family=self.spacecraft.family,
            spacecraft__version=self.spacecraft.version,
        ).count()
        family_type_launch_num = SpacecraftOnLaunch.objects.filter(
            launch__time__lte=self.launch.time,
            spacecraft__family=self.spacecraft.family,
            spacecraft__type=self.spacecraft.type,
        ).count()
        family_reuse_num = SpacecraftOnLaunch.objects.filter(
            launch__time__lte=self.launch.time, spacecraft__family=self.spacecraft.family, num_flights__gt=1
        ).count()
        boat_recovery_num = SpacecraftOnLaunch.objects.filter(
            launch__time__lte=self.launch.time,
            spacecraft__family=self.spacecraft.family,
            recovery_boat=self.recovery_boat,
        ).count()

        stats = [
            (
                is_significant(family_launch_num),
                f"{make_ordinal(family_launch_num)} launch of {self.spacecraft.family}",
            ),
            (
                is_significant(family_version_launch_num),
                f"{make_ordinal(family_version_launch_num)} launch of {self.spacecraft.family} {self.spacecraft.version}",
            ),
            (
                is_significant(family_type_launch_num),
                f"{make_ordinal(family_type_launch_num)} launch of {self.spacecraft.type.title()} {self.spacecraft.family}",
            ),
        ]

        if self.num_flights and self.num_flights > 1:
            stats.append(
                (
                    is_significant(family_reuse_num),
                    f"{make_ordinal(family_reuse_num)} reuse of a {self.spacecraft.family} spacecraft",
                )
            )

        if self.recovery_boat:
            stats.append(
                (
                    is_significant(boat_recovery_num),
                    f"{make_ordinal(boat_recovery_num)} recovery of a {self.spacecraft.family} spacecraft by {self.recovery_boat}",
                )
            )

        return stats


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
