import pytz
from .models import *
from datetime import datetime


def format_time(time_obj):
    formatted_date = time_obj.strftime("%B %d, %Y")
    formatted_time = time_obj.strftime("%H:%M")
    timezone_abbr = time_obj.strftime("%Z")
    
    formatted_str = f"{formatted_date} - {formatted_time} {timezone_abbr}"

    return formatted_str

def make_ordinal(n: int):
    if n is None:
        return "None"
    elif 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

def get_stage_flights_and_turnaround(stage: Stage, launch: Launch) -> tuple:
    flights = 0
    turnaround: str = "N/A"

    launches = Launch.objects.filter(stageandrecovery__stage=stage).order_by('time')

    for index, launch1 in enumerate(launches):
        if launch1.time <= launch.time:
            flights += 1
        if (not index == 0) and launch.time == launch1.time:
            delta = launch.time-launches[index-1].time
            turnaround = str(round(delta.total_seconds() / 86400, 2))
            return(flights, turnaround)
    else:
        return (flights, "N/A")

def create_launch_table(launch: Launch) -> str:
    time_zone = None
    boosters_display = ""
    launch_location = ""
    launch_landings = "The first stage will be expended"
    droneship_needed: bool = False
    fairing_recovery: bool = False

    for stage in Stage.objects.filter(stageandrecovery__launch=launch):
        boosters_display += stage.name + "-" + f"{get_stage_flights_and_turnaround(stage, launch)[0]}" + ", "
    boosters_display = boosters_display.rstrip(" ").rstrip(",")
    if len(Stage.objects.filter(stageandrecovery__launch=launch)):
        boosters_display += "; "

    for stage in Stage.objects.filter(stageandrecovery__launch=launch):
        boosters_display += f"{get_stage_flights_and_turnaround(stage, launch)[1]}, "

    boosters_display = boosters_display.rstrip(" ").rstrip(",").replace("None", "N/A")
    if len(Stage.objects.filter(stageandrecovery__launch=launch)):
        boosters_display += "-day turnaround"
    else:
        boosters_display = "Unknown booster"

    if launch.pad.nickname == "SLC-4E":
        launch_location = "Space Launch Complex 4 East (SLC-4E), Vandenberg Space Force Base, California, USA"
        time_zone = "US/Pacific"
    elif launch.pad.nickname == "SLC-40":
        launch_location = "Space Launch Complex 40 (SLC-40), Cape Canaveral Space Force Station, Florida, USA"
        time_zone = "US/Eastern"
    elif launch.pad.nickname == "LC-39A":
        launch_location = "Launch Complex 39A (LC-39A), Kennedy Space Center, Florida, USA"
        time_zone = "US/Eastern"
    elif launch.pad.nickname == "OLP-A":
        launch_location = "Orbital Launch Pad A, Starbase, Texas, USA"
        time_zone = "US/Central"
    elif launch.pad.name == "Omelek Island":
        launch_location = "Omelex Island, Kwajalein Atoll, Republic of the Marshall Islands"
        time_zone = "Etc/GMT+12"

    time_zone = pytz.timezone(time_zone)

    liftoff_time_local = launch.time.astimezone(time_zone)

    def success(value: bool) -> str:
        if value == True:
            return "successfully completed"
        return "failed to complete"

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
                if item.landing_zone is not None:
                    launch_landings += f"{item.stage.name} will be recovered on {item.landing_zone.name} ({item.landing_zone.nickname}); "
            else:
                if item.landing_zone is not None:
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
                if item.landing_zone is not None:
                    launch_landings += f"{item.stage.name} {success(item.method_success)} a landing on {item.landing_zone.name} ({item.landing_zone.nickname}); "
            else:
                if item.landing_zone is not None:
                    launch_landings += f"{item.stage.name} {success(item.method_success)} a landing on {item.landing_zone.name} ({item.landing_zone.nickname}); "

    if not len(FairingRecovery.objects.filter(launch=launch)) == 0:
        fairing_recovery = True

    launch_landings: list = launch_landings.rstrip("; ")

    concatinated_list = lambda boats: ', '.join(map(str, boats[:-1])) + (' and ' if len(boats) > 1 else '') + str(boats[-1]) if boats else 'N/A'
    
    def make_list(objects: Boat) -> list:
        names: set[str] = set()
        for item in objects:
            names.add(item.boat.name)
        return list(names)

    data = {
        "Lift Off Time": [f"{format_time(launch.time)}", f"{format_time(liftoff_time_local)}"],
        "Mission Name": [launch.name],
        "Launch Provider <br /> (What rocket company is launching it?)": ["SpaceX"],
        "Customer <br /> (Who's paying for this?)": [launch.customer],
        "Rocket": [f"{launch.rocket}; {boosters_display}"],
        "Launch Location": [f"{launch_location}"],
        "Payload mass": [f"{launch.mass}"],
        "Where are the satellites going?": [f"{launch.orbit}"],
        "Where will the first stage land?": [f"{launch_landings}"],
        "Will they be attempting to recover the fairings?": [],
        "How's the weather looking?": ["The weather is currently XX% go for launch"],
        "This will be the": []
    }

    if droneship_needed == True:
        data["Where will the first stage land?"].append("")
        data["Where will the first stage land?"].append(f"Tug: {concatinated_list(make_list(TugOnLaunch.objects.filter(launch=launch)))}; Support: {concatinated_list(make_list(SupportOnLaunch.objects.filter(launch=launch)))}")
    
    if fairing_recovery == True and launch.time > datetime.now(pytz.utc):
        data["Will they be attempting to recover the fairings?"].append(f"The fairing halves will be recovered from the water by {concatinated_list(make_list(FairingRecovery.objects.filter(launch=launch)))}")
    elif fairing_recovery == True and launch.time < datetime.now(pytz.utc):
        data["Will they be attempting to recover the fairings?"].append(f"The fairing halves were recovered by {concatinated_list(make_list(FairingRecovery.objects.filter(launch=launch)))}")
    else:
        data["Will they be attempting to recover the fairings?"].append("There are no fairings on this flight")

    if launch.pad.nickname == "SLC-4E":
        data["How's the weather looking?"][0] = "Space Launch Delta 30 does not release public weather forecasts"
    elif launch.pad.nickname == "OLP-A" or launch.pad.name == "Omelek Island":
        data["How's the weather looking?"][0] = "Unknown"

    stats: list[str] = []

    def get_rocket_launch_num() -> str:
        count: int = 0
        for launch1 in Launch.objects.filter(rocket=launch.rocket):
            if launch1.time <= launch.time:
                count += 1
        return make_ordinal(count)
    
    def get_rocket_flights_reused_vehicle() -> tuple:
        count = 0
        stages_seen: set = set()
        booster_flight_proven: bool = False

        for launch1 in Launch.objects.filter(time__lt=launch.time).order_by('time'):
            if StageAndRecovery.objects.filter(launch=launch1).exists():
                value_added: bool = False
                for stage_and_recovery in StageAndRecovery.objects.filter(launch=launch1, stage__type="BOOSTER"):
                    if stage_and_recovery.stage.name in stages_seen and launch1.rocket == launch.rocket and value_added == False:
                        count += 1
                        value_added = True
                    stages_seen.add(stage_and_recovery.stage.name)

        if StageAndRecovery.objects.filter(launch=launch).exists():
            for stage_and_recovery in StageAndRecovery.objects.filter(launch=launch):
                if stage_and_recovery.stage.name in stages_seen:
                    booster_flight_proven = True
                    count += 1
                    break

                
        return (make_ordinal(count), booster_flight_proven)
    
    def get_total_reflights(start: datetime=datetime(2000, 1, 1, tzinfo=pytz.UTC), end: datetime=launch.time) -> str:
        count = 0
        count_list: list[str] = []
        stages_seen: set = set()

        for launch1 in Launch.objects.filter(time__lt=launch.time).order_by('time'):
            for stage_and_recovery in StageAndRecovery.objects.filter(launch=launch1, stage__type="BOOSTER"):
                if stage_and_recovery.stage.name in stages_seen:
                    if launch1.time >= start and launch1.time < end:
                        count += 1
                stages_seen.add(stage_and_recovery.stage.name)
        if StageAndRecovery.objects.filter(launch=launch).exists():
            for stage_and_recovery in StageAndRecovery.objects.filter(launch=launch):
                if stage_and_recovery.stage.name in stages_seen:
                    count += 1
                    count_list.append(make_ordinal(count))
        return concatinated_list(count_list)
    
    def get_num_booster_landings():
        count: int = 0
        count_list: list[str] = []
        for launch1 in Launch.objects.filter(time__lt=launch.time).order_by('time'):
            if StageAndRecovery.objects.filter(launch=launch1, stage__type="BOOSTER").exists():
                for landing in StageAndRecovery.objects.filter(launch=launch1, stage__type="BOOSTER"):
                    if (landing.method == "DRONE_SHIP" or landing.method == "GROUND_PAD") and landing.method_success == True:
                        count += 1
        if StageAndRecovery.objects.filter(launch=launch, stage__type="BOOSTER").exists():
            for landing in StageAndRecovery.objects.filter(launch=launch, stage__type="BOOSTER"):
                if (landing.method == "DRONE_SHIP" or landing.method == "GROUND_PAD") and (landing.method_success == True or launch.time > datetime.now(pytz.utc)):
                    count += 1
                    count_list.append(make_ordinal(count))
            if not len(count_list) == 0:
                return concatinated_list(count_list)
            else:
                return None
            
    def get_consec_landings():
        count: int = 0
        count_list: list[str] = []
        flag: bool = False

        for launch1 in Launch.objects.filter(time__lt=launch.time).order_by('-time'):
            if StageAndRecovery.objects.filter(launch=launch1, stage__type="BOOSTER").exists():
                for landing in StageAndRecovery.objects.filter(launch=launch1, stage__type="BOOSTER"):
                    if (landing.method == "DRONE_SHIP" or landing.method == "GROUND_PAD") and landing.method_success == True:
                        count += 1
                    elif (landing.method == "DRONE_SHIP" or landing.method == "GROUND_PAD") and landing.method_success == False:
                        flag = True
                        break
                if flag:
                    break
                
        if StageAndRecovery.objects.filter(launch=launch, stage__type="BOOSTER"):
            for landing in StageAndRecovery.objects.filter(launch=launch, stage__type="BOOSTER"):
                if (landing.method == "DRONE_SHIP" or landing.method == "GROUND_PAD") and (landing.method_success == True or launch.time > datetime.now(pytz.utc)):
                    count += 1
                    count_list.append(make_ordinal(count))
            if len(count_list) == 1:
                return concatinated_list(count_list), ""
            if len(count_list) > 1:
                return concatinated_list(count_list), "s"
            
    def get_year_launch_num() -> str:
        count: int = 0
        for _ in Launch.objects.filter(time__gte=datetime(launch.time.year, 1, 1, tzinfo=pytz.utc), time__lte=launch.time):
            count += 1
        return make_ordinal(count)
    
    def get_launches_from_pad() -> str:
        count: int = 0
        for _ in Launch.objects.filter(pad=launch.pad, time__lte=launch.time):
            count += 1
        return make_ordinal(count)


    booster_reuse = get_rocket_flights_reused_vehicle()
    booster_landings = get_num_booster_landings()

    #Stats:
    stats.append(f"– {get_rocket_launch_num()} {launch.rocket.name} mission")
    if booster_reuse[1] == True:
        stats.append(f"– {booster_reuse[0]} {launch.rocket} flight with a flight-proven booster")
        stats.append(f"– {get_total_reflights()} reflight of a booster")
        stats.append(f"– {get_total_reflights(datetime(launch.time.year, 1, 1, tzinfo=pytz.UTC), datetime(launch.time.year+1, 1, 1, tzinfo=pytz.UTC))} reflight of a booster in {launch.time.year}")
    
    if booster_landings:
        stats.append(f"– {booster_landings} booster landing{get_consec_landings()[1]}")
        stats.append(f"– {get_consec_landings()[0]} consecutive booster landing{get_consec_landings()[1]}")
    stats.append(f"– {get_year_launch_num()} SpaceX launch of {launch.time.year}")
    stats.append(f"– {get_launches_from_pad()} SpaceX launch from {launch.pad.name}")


    data["This will be the"] = stats

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
        "This was the"
    ]

    if launch.time < datetime.now(pytz.utc):
        ordered_data = {new_key: data.get(old_key, None) for old_key, new_key in zip(data.keys(), post_launch_data)}
        ordered_data.pop("How's the weather looking?", None)

        data = ordered_data


    # Generate HTML table
    table_html = "<table>"
    for key, values in data.items():
        table_html += "<tr><th class=\"has-text-align-left\" data-align=\"left\"><h6><strong>{}</strong></h6></th>".format(key)
        table_html += "<td>"
        for value in values:
            table_html += "<em>{}</em><br>".format(value)
        table_html += "</td></tr>"
    table_html += "</table>"

    return table_html