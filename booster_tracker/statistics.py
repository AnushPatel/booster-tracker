import pytz
from .models import *
from datetime import datetime
from enum import StrEnum
from django.db.models import Q

#First several functions will be defined that are commonly used. 
#As the name implies, this formats the time to be in the following format: March 25, 2024 04:38 UTC
def format_time(time_obj):
    formatted_date = time_obj.strftime("%B %d, %Y")
    formatted_time = time_obj.strftime("%H:%M")
    timezone_abbr = time_obj.strftime("%Z")
    
    formatted_str = f"{formatted_date} - {formatted_time} {timezone_abbr}"

    return formatted_str

#This converts from seconds to a human readable format in days, hours, minutes, and seconds. If any are zero, they are removed.
def convert_seconds(x):
    d = int(x/86400)
    x -= (d*86400)
    h = int(x/3600)
    x -= (h*3600)
    m = int(x/60)
    x -= (m*60)
    s = round(x)
    
    time_str = ""
    if d:
        time_str += f"{d} day{'s' if d != 1 else ''}, "
    if h:
        time_str += f"{h} hour{'s' if h != 1 else ''}, "
    if m:
        time_str += f"{m} minute{'s' if m != 1 else ''}, "
    if s:
        time_str += f"and {s} second{'s' if s != 1 else ''}"

    if time_str[-2:] == ", ":
        time_str = time_str[:-2]
    
    return time_str

#Makes an ordinal; 1 -> 1st
def make_ordinal(n: int):
    if n is None:
        return "None"
    elif 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

#Takes in a list of items and returns them in concatinated form [Bob, Doug, GO Beyond] -> Bob, Doug, and GO Beyond
concatinated_list = lambda items: ', '.join(items[:-1]) + (' and ' if len(items) > 1 else '') + str(items[-1]) if items else 'N/A'

#This item creates a list without any repeats
def make_list(objects: Boat) -> list:
    names: set[str] = set()
    for item in objects:
        names.add(item.boat.name)
    return list(names)

#Helps convert boolean to human readable text in stats
def success(value: bool) -> str:
    if value == True:
        return "successfully completed"
    return "failed to complete"

#This section we create StrEnums to limit options in functions
class TurnaroundObjects(StrEnum):
    BOOSTER = "booster"
    SECOND_STAGE = "second stage"
    LANDING_ZONE = "landing zone"
    PAD = "pad"
    ALL = "all"

#This section we start defining functions to create stats:
#Simply gets the turnaround time between two objects; the exact list should be specified elsewhere
def turnaround_time(launches: list[Launch]) -> int:
    if len(launches) > 1:
        return((launches[len(launches)-1].time-launches[len(launches)-2].time).total_seconds())
    return None

#This function gets number of time a stage and flown, and what the most recent turnaround is
def get_stage_flights_and_turnaround(stage: Stage, time: datetime) -> tuple:
    flights = 0
    turnaround = "N/A"

    turnaround = turnaround_time(Launch.objects.filter(stageandrecovery__stage=stage, time__lte=time).order_by('time'))
    if turnaround:
        turnaround = round(turnaround / 86400, 2)
    flights += Launch.objects.filter(stageandrecovery__stage=stage, time__lte=time).count()

    return(flights, turnaround)

#Get the number of times a rocket has flown with AT LEAST one flight proven booster; so this increments by one regardless of if Falcon Heavy has one or three flight proven boosters.
def get_rocket_flights_reused_vehicle(launch: Launch) -> tuple:
    count = 0
    stages_seen: set = set()
    booster_flight_proven: bool = False

    value_added: bool = False
    previous_launch: Launch = None
    for stage_and_recovery in StageAndRecovery.objects.filter(launch__time__lt=launch.time, stage__type="BOOSTER").order_by("launch__time").all():
        if previous_launch != stage_and_recovery.launch:
            value_added = False
        if stage_and_recovery.stage in stages_seen and not value_added and launch.rocket == stage_and_recovery.launch.rocket:
            count += 1
            value_added = True
        stages_seen.add(stage_and_recovery.stage)
        previous_launch = stage_and_recovery.launch

    if StageAndRecovery.objects.filter(launch=launch, stage__in=stages_seen).exists():
        booster_flight_proven = True
        count += 1

    return (make_ordinal(count), booster_flight_proven)

#This function looks at TOTAL number of booster reflights; so increments by two if two boosters on Falcon Heavy are flight proven.
def get_total_reflights(launch: Launch, start: datetime) -> str:
    count = 0
    count_list: list[str] = []
    stages_seen: set = set()
    end = launch.time

    for stage_and_recovery in StageAndRecovery.objects.filter(launch__time__lt=launch.time, stage__type="BOOSTER").order_by("launch__time").all():
        if stage_and_recovery.stage in stages_seen:
            if stage_and_recovery.launch.time > start and stage_and_recovery.launch.time < end:
                count += 1
        stages_seen.add(stage_and_recovery.stage)

    for stage_and_recovery in StageAndRecovery.objects.filter(launch=launch, stage__in=stages_seen):
        count += 1
        count_list.append(make_ordinal(count))
    return concatinated_list(count_list)

#Counts number of booster landings
def get_num_booster_landings(launch: Launch):   
    count: int = 0
    count_list: list[str] = []

    count += StageAndRecovery.objects.filter(launch__time__lt=launch.time, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).filter(method_success=True).count()

    for _ in StageAndRecovery.objects.filter(launch=launch, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).filter(Q(method_success=True) | Q(launch__time__gte=datetime.now(pytz.utc))):
        count += 1
        count_list.append(make_ordinal(count))
    if not len(count_list) == 0:
        return concatinated_list(count_list)
    return None

#Gets number of launches in a year and from a pad
def get_year_launch_num(launch: Launch) -> str:
    return make_ordinal(Launch.objects.filter(time__gte=datetime(launch.time.year, 1, 1, tzinfo=pytz.utc), time__lte=launch.time).count())

def get_launches_from_pad(launch: Launch) -> str:
    return make_ordinal(Launch.objects.filter(pad=launch.pad, time__lte=launch.time).count())

#Returns list of turnaround times for object type
def calculate_turnarounds(object: TurnaroundObjects, launch: Launch):
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
            launches = Launch.objects.filter(stageandrecovery__stage=item, time__lte=launch.time).order_by("time").all()
        elif isinstance(item, Pad):
            launches = Launch.objects.filter(pad=item, time__lte=launch.time).order_by("time").all()
        elif isinstance(item, LandingZone):
            launches = Launch.objects.filter(stageandrecovery__landing_zone=item, time__lte=launch.time).order_by("time").all()
        else:
            launches = Launch.objects.filter(time__lte=launch.time).order_by("time").all()
        
        for i in range(0, len(launches)+1):
            turnaround = turnaround_time(launches=launches[:i])
            if turnaround and object != TurnaroundObjects.ALL:
                turnarounds.append([getattr(item, name_field), turnaround, launches[i-1].name, launches[i-2].name])
            elif turnaround:
                turnarounds.append(["", turnaround, launches[i-1].name, launches[i-2].name])

    turnarounds = sorted(turnarounds, key=lambda x: (x[1] is None, x[1] if x[1] is not None else float('inf')))

        
    if turnarounds[0][2] == launch.name:
        new_record = True

    if not len(turnarounds) == 0:
        return new_record, turnarounds
    return None

#This function gets the number of landings in a row; there may be some bad logic here if, say, a Falcon Heavy side booster fails to land but the center core lands successfully. If this ever happens, look here!
def get_consec_landings(launch: Launch):
    count: int = 0
    count_list: list[str] = []

    for landing in StageAndRecovery.objects.filter(launch__time__lt=launch.time, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).order_by("-launch__time").all():
        if landing.method_success:
            count += 1
        else:
            break

    for landing in StageAndRecovery.objects.filter(launch=launch, stage__type="BOOSTER").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")):
        if landing.method_success or launch.time > datetime.now(pytz.utc):
            count += 1
            count_list.append(make_ordinal(count))
    if len(count_list) == 1:
        return concatinated_list(count_list), ""
    if len(count_list) > 1:
        return concatinated_list(count_list), "s"

#This section uses the functions above to create the EDA-style launch table for each launch!
def create_launch_table(launch: Launch) -> str:
    time_zone = None
    boosters_display = ""
    launch_location = ""
    launch_landings = "The first stage will be expended"
    droneship_needed: bool = False

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

    #Configure the display of stages. For exmaple, formatting as B1067-20; 20.42 day turnaround
    for stage in Stage.objects.filter(stageandrecovery__launch=launch):
        boosters_display += stage.name + "-" + f"{get_stage_flights_and_turnaround(stage=stage, time=launch.time)[0]}" + ", "
    boosters_display = boosters_display.rstrip(" ").rstrip(",")

    if Stage.objects.filter(stageandrecovery__launch=launch).count():
        boosters_display += "; "

    for stage in Stage.objects.filter(stageandrecovery__launch=launch):
        boosters_display += f"{get_stage_flights_and_turnaround(stage=stage, time=launch.time)[1]}, "

    boosters_display = boosters_display.rstrip(" ").rstrip(",").replace("None", "N/A")
    if len(Stage.objects.filter(stageandrecovery__launch=launch)):
        boosters_display += "-day turnaround"
    else:
        boosters_display = "Unknown booster"

    #Configure timezone for local time conversion. I also change what default weather says based on the location 
    if launch.pad.nickname == "SLC-4E":
        launch_location = "Space Launch Complex 4 East (SLC-4E), Vandenberg Space Force Base, California, USA"
        time_zone = "US/Pacific"
        data["How's the weather looking?"][0] = "Space Launch Delta 30 does not release public weather forecasts"
    elif launch.pad.nickname == "SLC-40":
        launch_location = "Space Launch Complex 40 (SLC-40), Cape Canaveral Space Force Station, Florida, USA"
        time_zone = "US/Eastern"
    elif launch.pad.nickname == "LC-39A":
        launch_location = "Launch Complex 39A (LC-39A), Kennedy Space Center, Florida, USA"
        time_zone = "US/Eastern"
    elif launch.pad.nickname == "OLP-A":
        launch_location = "Orbital Launch Pad A, Starbase, Texas, USA"
        time_zone = "US/Central"
        data["How's the weather looking?"][0] = "Unknown"
    elif launch.pad.name == "Omelek Island":
        launch_location = "Omelex Island, Kwajalein Atoll, Republic of the Marshall Islands"
        time_zone = "Etc/GMT+12"
        data["How's the weather looking?"][0] = "Unknown"

    time_zone = pytz.timezone(time_zone)
    liftoff_time_local = launch.time.astimezone(time_zone)

    #Figure out where stages will land or where they landed; change tense based on portion of time. Accounts for soft ocean landings as well
    for item in StageAndRecovery.objects.filter(launch=launch):
        if launch.time > datetime.now(pytz.utc):
            if launch_landings == "The first stage will be expended":
                launch_landings = ""
            if item.method == "EXPENDED":
                launch_landings += f"{item.stage.name} will be expended; "
            elif item.method == "OCEAN_SURFACE":
                launch_landings += f"{item.stage.name} will attempt a soft landing on the ocean surface; "
            elif item.method == "DRONE_SHIP":
                droneship_needed = True
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
                droneship_needed = True
                if item.landing_zone:
                    launch_landings += f"{item.stage.name} {success(item.method_success)} a landing on {item.landing_zone.name} ({item.landing_zone.nickname}); "
            else:
                if item.landing_zone:
                    launch_landings += f"{item.stage.name} {success(item.method_success)} a landing on {item.landing_zone.name} ({item.landing_zone.nickname}); "
    launch_landings: list = launch_landings.rstrip("; ")

    #Update data with everything known
    data["Lift Off Time"] = [f"{format_time(launch.time)}", f"{format_time(liftoff_time_local)}"]
    data["Mission Name"] = [launch.name]
    data["Customer <br /> (Who's paying for this?)"] = [launch.customer]
    data["Rocket"] = [f"{launch.rocket}; {boosters_display}"]
    data["Launch Location"] = [f"{launch_location}"]
    data["Payload mass"] = [launch.mass]
    data["Where are the satellites going?"] = [launch.orbit.name]
    data["Where will the first stage land?"] = [f"{launch_landings}"]

    if droneship_needed:
        data["Where will the first stage land?"].append("")
        data["Where will the first stage land?"].append(f"Tug: {concatinated_list(make_list(TugOnLaunch.objects.filter(launch=launch)))}; Support: {concatinated_list(make_list(SupportOnLaunch.objects.filter(launch=launch)))}")
    
    if not len(FairingRecovery.objects.filter(launch=launch)) == 0 and launch.time > datetime.now(pytz.utc):
        data["Will they be attempting to recover the fairings?"].append(f"The fairing halves will be recovered from the water by {concatinated_list(make_list(FairingRecovery.objects.filter(launch=launch)))}")
    elif not len(FairingRecovery.objects.filter(launch=launch)) == 0 and launch.time < datetime.now(pytz.utc):
        data["Will they be attempting to recover the fairings?"].append(f"The fairing halves were recovered by {concatinated_list(make_list(FairingRecovery.objects.filter(launch=launch)))}")
    else:
        data["Will they be attempting to recover the fairings?"].append("There are no fairings on this flight")

    #Finally, calculate stats for the mission; these are stored in an array like everything else above
    stats: list[str] = []

    booster_reuse = get_rocket_flights_reused_vehicle(launch=launch) 
    booster_landings = get_num_booster_landings(launch=launch)

    stats.append(f"– {make_ordinal(Launch.objects.filter(rocket=launch.rocket, time__lte=launch.time).count())} {launch.rocket.name} mission")
    if booster_reuse[1]:
        stats.append(f"– {booster_reuse[0]} {launch.rocket} flight with a flight-proven booster")
        stats.append(f"– {get_total_reflights(launch=launch, start=datetime(2000, 1, 1, tzinfo=pytz.utc))} reflight of a booster")
        stats.append(f"– {get_total_reflights(launch=launch, start=datetime(launch.time.year, 1, 1, tzinfo=pytz.utc))} reflight of a booster in {launch.time.year}")

    if booster_landings:
        consec_landings = get_consec_landings(launch=launch)
        stats.append(f"– {booster_landings} booster landing{consec_landings[1]}")
        stats.append(f"– {consec_landings[0]} consecutive booster landing{consec_landings[1]}")
    stats.append(f"– {get_year_launch_num(launch=launch)} SpaceX launch of {launch.time.year}")
    stats.append(f"– {get_launches_from_pad(launch=launch)} SpaceX launch from {launch.pad.name}")

    #This section adds quickest turnaround stats. As the names imply, booster, zones, company, and pad.

    booster_turnarounds = calculate_turnarounds(object=TurnaroundObjects.BOOSTER, launch=launch)
    if booster_turnarounds[0]:
        booster_string = f"– Qickest turnaround of a booster to date at {convert_seconds(booster_turnarounds[1][0][1])}"
        if len(booster_turnarounds[1]) > 1:
            booster_string += f". Previous record: {booster_turnarounds[1][1][0]} at {convert_seconds(booster_turnarounds[1][1][1])} between {booster_turnarounds[1][1][3]} and {booster_turnarounds[1][1][2]}"
        stats.append(booster_string)
    else:
        for recovery in StageAndRecovery.objects.filter(launch=launch):
            specific_booster_turnarounds = [row for row in booster_turnarounds[1] if f"{recovery.stage.name}" == row[0]]
            if len(specific_booster_turnarounds) > 0 and specific_booster_turnarounds[0][2] == launch.name:
                booster_string = f"– Quickest turnaround of {recovery.stage.name} to date at {convert_seconds(specific_booster_turnarounds[0][1])}"
                if len(specific_booster_turnarounds) > 1:
                    booster_string += f". Previous record: {convert_seconds(specific_booster_turnarounds[1][1])} between {specific_booster_turnarounds[1][3]} and {specific_booster_turnarounds[1][2]}"
                stats.append(booster_string)

    landing_zone_turnarounds = calculate_turnarounds(TurnaroundObjects.LANDING_ZONE, launch)
    if landing_zone_turnarounds[0]:
        zone_string = f"– Quickest turnaround time of a landing zone to date at {convert_seconds(landing_zone_turnarounds[1][0][1])}"
        if len(landing_zone_turnarounds) > 1:
            zone_string += f". Previous record: {landing_zone_turnarounds[1][1][0]} at {convert_seconds(landing_zone_turnarounds[1][1][1])} between {landing_zone_turnarounds[1][1][3]} and {landing_zone_turnarounds[1][1][2]}"
        stats.append(zone_string)
    else:
        for recovery in StageAndRecovery.objects.filter(launch=launch):
            if recovery.landing_zone:
                specific_zone_turnarounds = [row for row in landing_zone_turnarounds[1] if f"{recovery.landing_zone.nickname}" == row[0]]
                if len(specific_zone_turnarounds) > 0 and specific_zone_turnarounds[0][2] == launch.name:
                    zone_string = f"– Qickest turnaround of {recovery.landing_zone.nickname} to date at {specific_zone_turnarounds[0][1]}"
                    if len(specific_zone_turnarounds) > 1:
                        zone_string += f". Previous record: {convert_seconds(specific_zone_turnarounds[1][1])} between {specific_zone_turnarounds[1][3]} and {specific_zone_turnarounds[1][2]}"
                    stats.append(zone_string)

    company_turnaround = calculate_turnarounds(object=TurnaroundObjects.ALL, launch=launch)
    if company_turnaround[0]:
        company_string = f"– Shortest time between any two SpaceX launches at {convert_seconds(company_turnaround[1][0][1])}"
        if len(company_turnaround[1]) > 1:
            company_string += f". Previous record: {convert_seconds(company_turnaround[1][1][1])} between {company_turnaround[1][1][3]} and {company_turnaround[1][1][2]}"
        stats.append(company_string)

    pad_turnarounds = calculate_turnarounds(object=TurnaroundObjects.PAD, launch=launch)
    if pad_turnarounds[0]:
        pad_string = f"– Qickest turnaround of a SpaceX pad to date at {convert_seconds(pad_turnarounds[1][0][1])}"
        if len(pad_turnarounds) > 1:
            pad_string += f". Previous record: {pad_turnarounds[1][1][0]} at {convert_seconds(pad_turnarounds[1][1][1])} between {pad_turnarounds[1][1][3]} and {pad_turnarounds[1][1][2]}"
        stats.append(pad_string)
    else:
        specific_pad_turnarounds = [row for row in pad_turnarounds[1] if f"{launch.pad.nickname}" == row[0]]
        if len(specific_pad_turnarounds) > 0 and specific_pad_turnarounds[0][2] == launch.name:
                pad_string = (f"– Qickest turnaround of {launch.pad.nickname} to date at {convert_seconds(specific_pad_turnarounds[0][1])}")
                if len(specific_pad_turnarounds) > 1:
                    pad_string += f". Previous record: {convert_seconds(specific_pad_turnarounds[1][1])} between {specific_pad_turnarounds[1][3]} and {specific_pad_turnarounds[1][2]}"
                stats.append(pad_string)
    data["This will be the"] = stats

    #Change title of headings if launch is in the past
    post_launch_data = [
        "Lift Off Time",
        "Mission Name",
        "Launch Provider <br /> (What rocket copmany launched it?)",
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

    if launch.time < datetime.now(pytz.utc):
        ordered_data = {new_key: data.get(old_key, None) for old_key, new_key in zip(data.keys(), post_launch_data)}
        ordered_data.pop("How's the weather looking?", None)

        data = ordered_data

    '''table_html = "<table>"
    for key, values in data.items():
        table_html += "<tr><th class=\"has-text-align-left\" data-align=\"left\"><h6><strong>{}</strong></h6></th>".format(key)
        table_html += "<td>"
        for value in values:
            table_html += "<em>{}</em><br>".format(value)
        table_html += "</td></tr>"
    table_html += "</table>"

    print(table_html)'''

    return data