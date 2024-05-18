from django.db import models
from generate_stats import turnaround_time, make_ordinal, concatenated_list, TurnaroundObjects, success, convert_seconds, format_time, remove_duplicates
from datetime import datetime
from django.db.models import Q, Count, Max
import pytz

# Create your models here.

RECOVERY_METHODS = [("EXPENDED", "expended"), ("OCEAN_SURFACE", "ocean"), ("DRONE_SHIP", "ASDS"), ("GROUND_PAD", "landing zone"), ("PARACHUTE", "parachute")]
LAUNCH_OUTCOMES = [("SUCCESS", "success"), ("FAILURE", "failure"), ("PARTIAL FAILURE", "partial failure")]
LANDING_METHOD_OUTCOMES = [("SUCCESS", "success"), ("FAILURE", "failure"), ("PRECLUDED", "precluded")]
BOAT_TYPES = [("TUG", "tug"), ("FAIRING_RECOVERY", "fairing recovery"), ("SUPPORT", "support")]
STAGE_TYPES = [("BOOSTER", "booster"), ("SECOND_STAGE", "second stage")]
SPACECRAFT_TYPES = [("CARGO", "cargo"), ("CREW", "crew")]
STAGE_LIFE_OPTIONS = [("ACTIVE", "active"), ("RETIRED", "retired"), ("EXPENDED", "expended"), ("LOST", "lost")]
LIFE_OPTIONS = [("ACTIVE", "active"), ("RETIRED", "retired")]

class Operator(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Rocket(models.Model):
    name = models.CharField(max_length=100)
    provider = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Stage(models.Model):
    name = models.CharField(max_length=20)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    version = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=STAGE_TYPES)
    status = models.CharField(max_length=20, choices=STAGE_LIFE_OPTIONS, default="ACTIVE")
    photo = models.ImageField(upload_to='stage_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Spacecraft(models.Model):
    name = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20, blank=True, null=True)
    version = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, choices=SPACECRAFT_TYPES)
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Boat(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=200, choices=BOAT_TYPES)
    def __str__(self):
        return self.name

class Orbit(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Pad(models.Model):
    name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=25)
    location = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=LIFE_OPTIONS, default="ACTIVE")
    image = models.ImageField(upload_to='pad_photos/', default='default.png')

    def __str__(self):
        return self.nickname

class Launch(models.Model):
    time = models.DateTimeField("Launch Time")
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    orbit = models.ForeignKey(Orbit, on_delete=models.CASCADE)
    mass = models.CharField(max_length=200)
    customer = models.CharField(max_length=200)
    launch_outcome = models.CharField(max_length=200, choices=LAUNCH_OUTCOMES, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Launches"
        ordering = ["-time"]

    def __str__(self):
        return self.name
    
    @property
    def image(self) -> str:
        return PadUsed.objects.get(pad=self.pad, rocket=self.rocket).image.url
    
    @property
    def droneship_needed(self) -> bool:
        return StageAndRecovery.objects.filter(launch=self, method="DRONE_SHIP").exists()
    
    @property
    def flight_proven_booster(self) -> bool:
        return (Stage.objects.filter(stageandrecovery__launch__time__lte=self.time).distinct().count() - Stage.objects.filter(stageandrecovery__launch__time__lt=self.time).distinct().count()) - Stage.objects.filter(stageandrecovery__launch=self).count() < 0
    
    @property
    def num_successful_landings(self) -> int:
        if self.time > datetime.now(pytz.utc):
            return StageAndRecovery.objects.filter(launch=self, stage__type="BOOSTER", method_success="SUCCESS").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).count()
        return StageAndRecovery.objects.filter(launch=self, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).count()

    #This function gets number of time a stage and flown, and what the most recent turnaround is
    def get_stage_flights_and_turnaround(self, stage: Stage) -> tuple:
        flights = 0
        time = self.time
        turnaround = turnaround_time(Launch.objects.filter(stageandrecovery__stage=stage, time__lte=time).order_by('time'))
        if turnaround:
            turnaround = round(turnaround / 86400, 2)
        flights += Launch.objects.filter(stageandrecovery__stage=stage, time__lte=time).count()

        return(flights, turnaround)
    
    #Get the number of times a rocket has flown with AT LEAST one flight proven booster; so this increments by one regardless of if Falcon Heavy has one or three flight proven boosters.
    def get_rocket_flights_reused_vehicle(self) -> tuple:
        count = 0
        stages_seen: set = set()

        value_added: bool = False
        previous_launch: Launch = None
        for stage_and_recovery in StageAndRecovery.objects.filter(launch__time__lt=self.time, stage__type="BOOSTER").order_by("launch__time").all():
            if previous_launch != stage_and_recovery.launch:
                value_added = False
            if stage_and_recovery.stage in stages_seen and not value_added and self.rocket == stage_and_recovery.launch.rocket:
                count += 1
                value_added = True
            stages_seen.add(stage_and_recovery.stage)
            previous_launch = stage_and_recovery.launch

        if StageAndRecovery.objects.filter(launch=self, stage__in=stages_seen).exists():
            count += 1

        return count
    
    #This function looks at TOTAL number of booster reflights; so increments by two if two boosters on Falcon Heavy are flight proven. The new stages seen is useful for when looking for reflights in a year; look at new boosters flown that year and subtracted.
    def get_total_reflights(self, start: datetime) -> str:
        count_list: list[str] = []
        stages_seen = list(Stage.objects.filter(type="BOOSTER", stageandrecovery__launch__time__lt=start).filter(rocket__name__icontains="Falcon").values_list("name", flat=True))
        new_stages_seen = list(Stage.objects.filter(type="BOOSTER", stageandrecovery__launch__time__lt=self.time, stageandrecovery__launch__time__gte=start).filter(rocket__name__icontains="Falcon").filter(~Q(name__in=stages_seen)).distinct().values_list("name", flat=True).all())
        num_booster_reflights = StageAndRecovery.objects.filter(launch__time__lt=self.time, launch__time__gt=start).filter(launch__rocket__name__icontains="Falcon").count() - Stage.objects.filter(type="BOOSTER", stageandrecovery__launch__time__lt=self.time, stageandrecovery__launch__time__gte=start).filter(rocket__name__icontains="Falcon").filter(~Q(name__in=stages_seen)).distinct().values_list("name", flat=True).all().count()

        for _ in StageAndRecovery.objects.filter(launch=self).filter(Q(stage__name__in=stages_seen)| Q(stage__name__in=new_stages_seen)):
            num_booster_reflights += 1
            count_list.append(make_ordinal(num_booster_reflights))
        return concatenated_list(count_list)
    
    #Counts number of booster landings
    def get_num_booster_landings(self):   
        count: int = 0
        count_list: list[str] = []

        count += StageAndRecovery.objects.filter(launch__time__lt=self.time, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).filter(method_success="SUCCESS").count()

        for _ in StageAndRecovery.objects.filter(launch=self, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).filter(Q(method_success="SUCCESS") | Q(launch__time__gte=datetime.now(pytz.utc))):
            count += 1
            count_list.append(make_ordinal(count))
        if not len(count_list) == 0:
            return concatenated_list(count_list)
        return None
    
    #Gets number of launches in a year and from a pad
    def get_year_launch_num(self) -> str:
        return make_ordinal(Launch.objects.filter(time__gte=datetime(self.time.year, 1, 1, tzinfo=pytz.utc), time__lte=self.time).count())

    def get_launches_from_pad(self) -> str:
        return make_ordinal(Launch.objects.filter(pad=self.pad, time__lte=self.time).count())
    
    #Returns list of turnaround times for object type
    def calculate_turnarounds(self, object: TurnaroundObjects):
        turnarounds: list = []
        new_record: bool = False
        queryset = None
        
        if object == TurnaroundObjects.BOOSTER:
            queryset = Stage.objects.filter(type="BOOSTER").distinct()
            name_field = "name"
        elif object == TurnaroundObjects.PAD:
            queryset = Pad.objects.all()
            name_field = "nickname"
        elif object == TurnaroundObjects.LANDING_ZONE:
            queryset = LandingZone.objects.all()
            name_field = "nickname"
        elif object == TurnaroundObjects.ALL:
            queryset = [""]
            name_field = "name"

        for item in queryset:
            if isinstance(item, Stage):  #If querying for stage, use stage field for filtering
                launches = Launch.objects.filter(stageandrecovery__stage=item, time__lte=self.time).order_by("time").all()
            elif isinstance(item, Pad):
                launches = Launch.objects.filter(pad=item, time__lte=self.time).order_by("time").all()
            elif isinstance(item, LandingZone):
                launches = Launch.objects.filter(stageandrecovery__landing_zone=item, time__lte=self.time).order_by("time").all()
            else:
                launches = Launch.objects.filter(time__lte=self.time).order_by("time").all()
            
            for i in range(0, len(launches)+1):
                turnaround = turnaround_time(launches=launches[:i])
                if turnaround and object != TurnaroundObjects.ALL:
                    turnarounds.append([getattr(item, name_field), turnaround, launches[i-1].name, launches[i-2].name])
                elif turnaround:
                    turnarounds.append(["", turnaround, launches[i-1].name, launches[i-2].name])

        turnarounds = sorted(turnarounds, key=lambda x: (x[1] is None, x[1] if x[1] is not None else float('inf')))

        if turnarounds and turnarounds[0][2] == self.name:
            new_record = True

        if not len(turnarounds) == 0:
            return new_record, turnarounds
        return None
    
    #This function gets the number of landings in a row; there may be some bad logic here if, say, a Falcon Heavy side booster fails to land but the center core lands successfully. If this ever happens, add in order of landings to get correct value.
    def get_consec_landings(self):
        count: int = 0
        count_list: list[str] = []

        for landing in StageAndRecovery.objects.filter(launch__time__lt=self.time, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).order_by("-launch__time", "-id").all():
            if landing.method_success=="SUCCESS":
                count += 1
            else:
                break

        for landing in StageAndRecovery.objects.filter(launch=self, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")):
            if landing.method_success == "FAILURE":
                count = 0
            if landing.method_success == "SUCCESS" or self.time > datetime.now(pytz.utc):
                count += 1
                count_list.append(make_ordinal(count))
        return concatenated_list(count_list)
        
    #This function gets booster and recovery information
    def get_boosters(self):
        boosters = []
        for stage in Stage.objects.filter(stageandrecovery__launch=self):
                boosters.append(f"{stage}-{self.get_stage_flights_and_turnaround(stage=stage)[0]}")
        return concatenated_list(boosters)
    
    def get_recoveries(self):
        recoveries = []
        for stage_and_recovery in StageAndRecovery.objects.filter(launch=self):
            if stage_and_recovery.landing_zone:
                recoveries.append(f"{stage_and_recovery.landing_zone.nickname}")
            else:
                recoveries.append("Expended")
        return concatenated_list(recoveries)
    
    #Configure the display of stages. For exmaple, formatting as B1067-20; 20.42 day turnaround
    def make_booster_display(self) -> str:
        boosters_display = ""
        for stage in Stage.objects.filter(stageandrecovery__launch=self):
            boosters_display += stage.name + "-" + f"{self.get_stage_flights_and_turnaround(stage=stage)[0]}" + ", "
        boosters_display = boosters_display.rstrip(" ").rstrip(",")

        if Stage.objects.filter(stageandrecovery__launch=self).count():
            boosters_display += "; "

        for stage in Stage.objects.filter(stageandrecovery__launch=self):
            boosters_display += f"{self.get_stage_flights_and_turnaround(stage=stage)[1]}, "

        boosters_display = boosters_display.rstrip(" ").rstrip(",").replace("None", "N/A")
        if len(Stage.objects.filter(stageandrecovery__launch=self)):
            boosters_display += "-day turnaround"
        else:
            boosters_display = "Unknown booster"

        return boosters_display
    
    #Figure out where stages will land or where they landed; change tense based on portion of time. Accounts for soft ocean landings as well
    def make_landing_string(self):
        launch_landings = "The first stage will be expended"
        for item in StageAndRecovery.objects.filter(launch=self):
            if self.time > datetime.now(pytz.utc):
                if launch_landings == "The first stage will be expended":
                    launch_landings = ""
                if item.method == "EXPENDED":
                    launch_landings += f"{item.stage.name} will be expended; "
                elif item.method == "OCEAN_SURFACE":
                    launch_landings += f"{item.stage.name} will attempt a soft landing on the ocean surface; "
                elif item.method == "DRONE_SHIP":
                    if item.landing_zone:
                        launch_landings += f"{item.stage.name} will be recovered on {item.landing_zone.name} ({item.landing_zone.nickname}); "
                else:
                    if item.landing_zone:
                        launch_landings += f"{item.stage.name} will be recovered on {item.landing_zone.name} ({item.landing_zone.nickname}); "
            else:
                if launch_landings == "The first stage will be expended":
                    launch_landings = ""
                if item.method == "EXPENDED":
                    launch_landings += f"{item.stage.name} was expended; "
                elif item.method == "OCEAN_SURFACE":
                    launch_landings += f"{item.stage.name} {success(item.method_success)} a soft landing on the ocean surface; "
                elif item.method == "DRONE_SHIP":
                    if item.landing_zone:
                        launch_landings += f"{item.stage.name} {success(item.method_success)} a landing on {item.landing_zone.name} ({item.landing_zone.nickname}); "
                else:
                    if item.landing_zone:
                        launch_landings += f"{item.stage.name} {success(item.method_success)} a landing on {item.landing_zone.name} ({item.landing_zone.nickname}); "
        launch_landings: list = launch_landings.rstrip("; ")
        return launch_landings
    
    def make_stats(self) -> list:
        #Finally, calculate stats for the mission; these are stored in an array like everything else above
        stats: list[str] = []

        booster_reuse = self.get_rocket_flights_reused_vehicle() 
        booster_landings = self.get_num_booster_landings()

        stats.append(f"– {make_ordinal(Launch.objects.filter(rocket=self.rocket, time__lte=self.time).count())} {self.rocket.name} mission")
        if self.flight_proven_booster:
            stats.append(f"– {make_ordinal(booster_reuse)} {self.rocket} flight with a flight-proven booster")
            stats.append(f"– {self.get_total_reflights(start=datetime(2000, 1, 1, tzinfo=pytz.utc))} reflight of a booster")
            stats.append(f"– {self.get_total_reflights(start=datetime(self.time.year, 1, 1, tzinfo=pytz.utc))} reflight of a booster in {self.time.year}")

        if booster_landings:
            consec_landings = self.get_consec_landings()
            make_plural = "s" if self.num_successful_landings > 1 else ""
            stats.append(f"– {booster_landings} booster landing{make_plural}")
            stats.append(f"– {consec_landings} consecutive booster landing{make_plural}")
        stats.append(f"– {self.get_year_launch_num()} SpaceX launch of {self.time.year}")
        stats.append(f"– {self.get_launches_from_pad()} SpaceX launch from {self.pad.name}")

        #This section adds quickest turnaround stats. As the names imply, booster, zones, company, and pad.

        booster_turnarounds = self.calculate_turnarounds(object=TurnaroundObjects.BOOSTER)
        if booster_turnarounds:
            if booster_turnarounds[0]:
                booster_string = f"– Qickest turnaround of a booster to date at {convert_seconds(booster_turnarounds[1][0][1])}"
                if len(booster_turnarounds[1]) > 1:
                    booster_string += f". Previous record: {booster_turnarounds[1][1][0]} at {convert_seconds(booster_turnarounds[1][1][1])} between {booster_turnarounds[1][1][3]} and {booster_turnarounds[1][1][2]}"
                stats.append(booster_string)
            else:
                for recovery in StageAndRecovery.objects.filter(launch=self):
                    specific_booster_turnarounds = [row for row in booster_turnarounds[1] if f"{recovery.stage.name}" == row[0]]
                    if len(specific_booster_turnarounds) > 0 and specific_booster_turnarounds[0][2] == self.name:
                        booster_string = f"– Quickest turnaround of {recovery.stage.name} to date at {convert_seconds(specific_booster_turnarounds[0][1])}"
                        if len(specific_booster_turnarounds) > 1:
                            booster_string += f". Previous record: {convert_seconds(specific_booster_turnarounds[1][1])} between {specific_booster_turnarounds[1][3]} and {specific_booster_turnarounds[1][2]}"
                        stats.append(booster_string)

        landing_zone_turnarounds = self.calculate_turnarounds(TurnaroundObjects.LANDING_ZONE)
        if landing_zone_turnarounds:
            if landing_zone_turnarounds[0]:
                zone_string = f"– Quickest turnaround time of a landing zone to date at {convert_seconds(landing_zone_turnarounds[1][0][1])}"
                if len(landing_zone_turnarounds[1]) > 1:
                    zone_string += f". Previous record: {landing_zone_turnarounds[1][1][0]} at {convert_seconds(landing_zone_turnarounds[1][1][1])} between {landing_zone_turnarounds[1][1][3]} and {landing_zone_turnarounds[1][1][2]}"
                stats.append(zone_string)
            else:
                for recovery in StageAndRecovery.objects.filter(launch=self):
                    if recovery.landing_zone:
                        specific_zone_turnarounds = [row for row in landing_zone_turnarounds[1] if f"{recovery.landing_zone.nickname}" == row[0]]
                        if len(specific_zone_turnarounds) > 0 and specific_zone_turnarounds[0][2] == self.name:
                            zone_string = f"– Qickest turnaround of {recovery.landing_zone.nickname} to date at {convert_seconds(specific_zone_turnarounds[0][1])}"
                            if len(specific_zone_turnarounds) > 1:
                                zone_string += f". Previous record: {convert_seconds(specific_zone_turnarounds[1][1])} between {specific_zone_turnarounds[1][3]} and {specific_zone_turnarounds[1][2]}"
                            stats.append(zone_string)

        company_turnaround = self.calculate_turnarounds(object=TurnaroundObjects.ALL)
        if company_turnaround:
            if company_turnaround[0]:
                company_string = f"– Shortest time between any two SpaceX launches at {convert_seconds(company_turnaround[1][0][1])}"
                if len(company_turnaround[1]) > 1:
                    company_string += f". Previous record: {convert_seconds(company_turnaround[1][1][1])} between {company_turnaround[1][1][3]} and {company_turnaround[1][1][2]}"
                stats.append(company_string)

        pad_turnarounds = self.calculate_turnarounds(object=TurnaroundObjects.PAD)
        if pad_turnarounds:
            if pad_turnarounds[0]:
                pad_string = f"– Qickest turnaround of a SpaceX pad to date at {convert_seconds(pad_turnarounds[1][0][1])}"
                if len(pad_turnarounds[1]) > 1:
                    pad_string += f". Previous record: {pad_turnarounds[1][1][0]} at {convert_seconds(pad_turnarounds[1][1][1])} between {pad_turnarounds[1][1][3]} and {pad_turnarounds[1][1][2]}"
                stats.append(pad_string)
            else:
                specific_pad_turnarounds = [row for row in pad_turnarounds[1] if f"{self.pad.nickname}" == row[0]]
                if len(specific_pad_turnarounds) > 0 and specific_pad_turnarounds[0][2] == self.name:
                        pad_string = (f"– Qickest turnaround of {self.pad.nickname} to date at {convert_seconds(specific_pad_turnarounds[0][1])}")
                        if len(specific_pad_turnarounds) > 1:
                            pad_string += f". Previous record: {convert_seconds(specific_pad_turnarounds[1][1])} between {specific_pad_turnarounds[1][3]} and {specific_pad_turnarounds[1][2]}"
                        stats.append(pad_string)

        return stats
    
    #This section uses the functions above to create the EDA-style launch table for each launch!
    def create_launch_table(self) -> str:
        #Data contains table titles
        data = {
            "Lift Off Time": [],
            "Mission Name": [],
            "Launch Provider <br /> (What rocket company is launching it?)": ["SpaceX"],
            "Customer <br /> (Who's paying for this?)": [],
            "Rocket": [],
            "Launch Location": [],
            "Payload mass": [],
            "Where are the satellites going?": [],
            "Where will the first stage land?": [],
            "Will they be attempting to recover the fairings?": [],
            "How's the weather looking?": ["The weather is currently XX% go for launch"],
            "This will be the": [],
            "Where to watch": ["Official coverage"]
        }

        boosters_display = self.make_booster_display()
        launch_landings = self.make_landing_string()

        #Configure timezone for local time conversion. I also change what default weather says based on the location
        if self.pad.nickname == "SLC-4E":
            time_zone = "US/Pacific"
            data["How's the weather looking?"][0] = "Space Launch Delta 30 does not release public weather forecasts"
        elif self.pad.nickname == "SLC-40":
            time_zone = "US/Eastern"
        elif self.pad.nickname == "LC-39A":
            time_zone = "US/Eastern"
        elif self.pad.nickname == "OLP-A":
            time_zone = "US/Central"
            data["How's the weather looking?"][0] = "Unknown"
        elif self.pad.name == "Omelek Island":
            time_zone = "Etc/GMT+12"
            data["How's the weather looking?"][0] = "Unknown"

        launch_location = f"{self.pad.name} ({self.pad.nickname}), {self.pad.location}"
        time_zone = pytz.timezone(time_zone)
        liftoff_time_local = self.time.astimezone(time_zone)

        self.make_landing_string()

        #Update data with everything known
        data["Lift Off Time"] = [f"{format_time(self.time)}", f"{format_time(liftoff_time_local)}"]
        data["Mission Name"] = [self.name]
        data["Customer <br /> (Who's paying for this?)"] = [self.customer]
        data["Rocket"] = [f"{self.rocket}; {boosters_display}"]
        data["Launch Location"] = [f"{launch_location}"]
        data["Payload mass"] = [self.mass]
        data["Where are the satellites going?"] = [self.orbit.name]
        data["Where will the first stage land?"] = [f"{launch_landings}"]

        if self.droneship_needed:
            data["Where will the first stage land?"].append("")
            data["Where will the first stage land?"].append(f"Tug: {concatenated_list(remove_duplicates(Boat.objects.filter(tugonlaunch__launch=self)))}; Support: {concatenated_list(remove_duplicates(Boat.objects.filter(supportonlaunch__launch=self)))}")
        
        if not len(FairingRecovery.objects.filter(launch=self)) == 0 and self.time > datetime.now(pytz.utc):
            data["Will they be attempting to recover the fairings?"].append(f"The fairing halves will be recovered from the water by {concatenated_list(remove_duplicates(Boat.objects.filter(fairingrecovery__launch=self)))}")
        elif not len(FairingRecovery.objects.filter(launch=self)) == 0 and self.time < datetime.now(pytz.utc):
            data["Will they be attempting to recover the fairings?"].append(f"The fairing halves were recovered by {concatenated_list(remove_duplicates(Boat.objects.filter(fairingrecovery__launch=self)))}")
        else:
            data["Will they be attempting to recover the fairings?"].append("There are no fairings on this flight")

        stats = self.make_stats()
        
        data["This will be the"] = stats

        #Change title of headings if launch is in the past
        post_launch_data = [
            "Lift Off Time",
            "Mission Name",
            "Launch Provider <br /> (What rocket company launched it?)",
            "Customer <br /> (Who paid for this?)",
            "Rocket",
            "Launch Location",
            "Payload mass",
            "Where did the satellites go?",
            "Where did the first stage land?",
            "Did they attempt to recover the fairings?",
            "How's the weather looking?",
            "This was the",
            "Where to watch"
        ]

        if self.time < datetime.now(pytz.utc):
            ordered_data = {new_key: data.get(old_key, None) for old_key, new_key in zip(data.keys(), post_launch_data)}
            ordered_data.pop("How's the weather looking?", None)

            data = ordered_data

        table_html = "<table>"
        for key, values in data.items():
            table_html += "<tr><th class=\"has-text-align-left\" data-align=\"left\"><h6><strong>{}</strong></h6></th>".format(key)
            table_html += "<td>"
            for value in values:
                table_html += "<em>{}</em><br>".format(value)
            table_html += "</td></tr>"
        table_html += "</table>"

        print(table_html)
        return data

class LandingZone(models.Model):
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=20)
    serial_number = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=20, choices=LIFE_OPTIONS, default="ACTIVE")
    image = models.ImageField(upload_to='landing_zone_photos/', default='pad_photos/default.png')

    def __str__(self):
        return self.name

class StageAndRecovery(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True, blank=True)
    landing_zone = models.ForeignKey(LandingZone, on_delete=models.CASCADE, null=True, blank=True)
    method = models.CharField(max_length=200, choices=RECOVERY_METHODS)
    method_success = models.CharField(max_length=200, choices=LANDING_METHOD_OUTCOMES, null=True, blank=True)
    recovery_success = models.BooleanField()
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    def __str__(self):
        if self.stage and self.stage.name:
            return f"{self.stage.name} recovery"
        return("Unknown recovery")
    
class FairingRecovery(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "FAIRING_RECOVERY"}, null=True, blank=True)
    catch = models.BooleanField()
    recovery = models.CharField(max_length=200)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    flights = models.CharField(max_length=200)

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

    def __str__(self):
        if self.boat:
            return self.boat.name
        
class SupportOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    boat = models.ForeignKey(Boat, on_delete=models.CASCADE, limit_choices_to={"type": "SUPPORT"})

    class Meta:
        verbose_name_plural = "Support ships on launch"
    
    def __str__(self):
        if self.boat:
            return self.boat.name
    
class SpacecraftOnLaunch(models.Model):
    launch = models.ForeignKey(Launch, on_delete=models.CASCADE)
    spacecraft = models.ForeignKey(Spacecraft, on_delete=models.CASCADE)
    splashdown_time = models.DateTimeField("Splashdown Time", null=True)

    class Meta:
        verbose_name_plural = "Dragon on launch"
    
    def __str__(self):
        if self.spacecraft:
            return f"{self.spacecraft.name} on launch"
        
class PadUsed(models.Model):
    rocket = models.ForeignKey(Rocket, on_delete=models.CASCADE)
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rocket_pad_photos/', default='rocket_pad_photos/rocket_launch_image.jpg')

    class Meta:
        verbose_name_plural = "Pads used"
    
    def __str__(self):
        if self.pad:
            return f"{self.pad.name}"