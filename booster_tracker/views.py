from django.http import HttpResponse
from django.template import loader
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from .generate_stats import *

import pytz

from .models import *

from django.shortcuts import render
from .models import Launch

def launches_list(request):
    launches = Launch.objects.all().order_by("-time")
    context = {
        'launches': launches
    }

    return render(request, 'launches/launches_list.html', context)


def home(request):
    num_launches_per_rocket_and_successes: list = []
    num_landings_and_successes: list = [StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc)).filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).filter(~Q(method_success="PRECLUDED")).count(), StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc), method_success="SUCCESS").filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD")).count()]
    last_launch = Launch.objects.filter(time__lte=datetime.now(pytz.utc)).first()
    next_launch = Launch.objects.filter(time__gt=datetime.now(pytz.utc)).last()
    
    next_launch_boosters = get_boosters_and_recovery(launch=next_launch)[0].replace("N/A", "Unknown")
    next_launch_recoveries = get_boosters_and_recovery(launch=next_launch)[1]
    next_launch_tugs = concatenated_list(list(Boat.objects.filter(type="TUG", tugonlaunch__launch=next_launch).all().values_list("name", flat=True)))
    next_launch_fairing_recovery = concatenated_list(list(set(Boat.objects.filter(type="FAIRING_RECOVERY", fairingrecovery__launch=next_launch).all().values_list("name", flat=True))))
    next_launch_photo = 'rocket_pad_photos/rocket_launch_image.jpg'
    if next_launch:
        next_launch_photo = PadUsed.objects.get(pad=next_launch.pad, rocket=next_launch.rocket).image.url

    last_launch_boosters = get_boosters_and_recovery(launch=last_launch)[0]
    last_launch_recoveries = get_boosters_and_recovery(launch=last_launch)[1]
    last_launch_tugs = concatenated_list(list(Boat.objects.filter(type="TUG", tugonlaunch__launch=last_launch).all().values_list("name", flat=True)))
    last_launch_fairing_recovery = concatenated_list(list(set(Boat.objects.filter(type="FAIRING_RECOVERY", fairingrecovery__launch=last_launch).all().values_list("name", flat=True))))
    last_launch_photo = PadUsed.objects.get(pad=last_launch.pad, rocket=last_launch.rocket).image.url
    for rocket in Rocket.objects.all():
        num_launches_per_rocket_and_successes.append([rocket.name, Launch.objects.filter(rocket=rocket, time__lte=datetime.now(pytz.utc)).count(), Launch.objects.filter(rocket=rocket, launch_outcome="SUCCESS", time__lte=datetime.now(pytz.utc)).count()])
    
    #this section gets total number of reflights; it takes the number of booster uses and subtracts the number of boosters that have flown
    num_booster_uses = StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc)).filter(launch__rocket__name__icontains="Falcon").count()
    num_stages_used = Stage.objects.filter(type="BOOSTER", stageandrecovery__launch__time__lte=datetime.now(pytz.utc)).filter(rocket__name__icontains="Falcon").distinct().count()
    num_booster_reflights = num_booster_uses - num_stages_used
    most_flown_boosters = get_most_flown_boosters()
    most_flown_boosters_string = f"{concatenated_list(most_flown_boosters[0])}; {most_flown_boosters[1]} flights"
    quickest_booster_turnaround = calculate_turnarounds(object=TurnaroundObjects.BOOSTER, launch=last_launch)
    quickest_booster_turnaround_string = f"{quickest_booster_turnaround[1][0][0]} at {convert_seconds(quickest_booster_turnaround[1][0][1])}"

    falcon_9_reflights = get_rocket_flights_reused_vehicle(launch=Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Falcon 9").first())[0]
    falcon_heavy_reflights = get_rocket_flights_reused_vehicle(launch=Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Falcon Heavy").first())[0]

    pad_stats = []
    pads = Pad.objects.all()
    for pad in Pad.objects.all():
        turnarounds = calculate_turnarounds(object=TurnaroundObjects.PAD, launch=Launch.objects.filter(time__lte=datetime.now(pytz.utc), pad=pad).first())
        specific_pad_turnarounds = [row for row in turnarounds[1] if f"{pad.nickname}" == row[0]]
        pad_stats.append([pad.name, Launch.objects.filter(pad=pad, time__lte=datetime.now(pytz.utc)).count(), convert_seconds(specific_pad_turnarounds[0][1])])
    
    recovery_zone_stats = []
    recovery_zones = LandingZone.objects.all()
    for zone in LandingZone.objects.all():
        stage_and_recovery = StageAndRecovery.objects.filter(landing_zone=zone, launch__time__lte=datetime.now(pytz.utc)).last()
        if stage_and_recovery:
            launch = Launch.objects.filter(stageandrecovery=stage_and_recovery).first()
            turnarounds = calculate_turnarounds(object=TurnaroundObjects.LANDING_ZONE, launch=launch)
            specific_zone_turnarounds = [row for row in turnarounds[1] if f"{zone.nickname}" == row[0]]
            recovery_zone_stats.append([zone.name, Stage.objects.filter(stageandrecovery__landing_zone=zone, stageandrecovery__launch__time__lte=datetime.now(pytz.utc), stageandrecovery__method_success="SUCCESS").count(), convert_seconds(specific_zone_turnarounds[0][1])])

    shortest_time_between_launches = convert_seconds(calculate_turnarounds(object=TurnaroundObjects.ALL, launch=last_launch)[1][0][1])


    context = {
        'launches_per_vehicle': num_launches_per_rocket_and_successes,
        'num_landings': num_landings_and_successes,
        'num_booster_reflights': num_booster_reflights,
        'next_launch': next_launch,
        'last_launch': last_launch,
        'next_launch_boosters': next_launch_boosters,
        'next_launch_recoveries': next_launch_recoveries,
        'next_launch_tugs': next_launch_tugs,
        'next_launch_fairing_recovery': next_launch_fairing_recovery,
        'next_launch_photo': next_launch_photo,
        'last_launch_boosters': last_launch_boosters,
        'last_launch_recoveries': last_launch_recoveries,
        'last_launch_tugs': last_launch_tugs,
        'last_launch_fairing_recovery': last_launch_fairing_recovery,
        'last_launch_photo': last_launch_photo,
        'most_flown_boosters': most_flown_boosters_string,
        'quickest_booster_turnaround': quickest_booster_turnaround_string,
        'falcon_heavy_reflights': falcon_heavy_reflights,
        'falcon_9_reflights': falcon_9_reflights,
        'pad_stats': pad_stats,
        'pads': pads,
        'zone_stats': recovery_zone_stats,
        'recovery_zones': recovery_zones,
        'shortest_time_between_launches': shortest_time_between_launches
    }
    return render(request, 'launches/home.html', context=context)


def launch_details(request, launch_name):
    launch = get_object_or_404(Launch, name=launch_name)
    context = {'data': create_launch_table(launch=launch)}
    return render(request, 'launches/launch_table.html', context)
