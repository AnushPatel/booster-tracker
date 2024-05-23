from django.http import HttpResponse
from django.template import loader
from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import *

import pytz

from .models import *

from django.shortcuts import render
from .models import Launch

def launches_list(request):
    # Get the search query from the request
    query = request.GET.get('q')
    
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
    page_number = request.GET.get('page', 1)

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
        'paginated_launches': paginated_launches,
        'query': query,
    }

    return render(request, 'launches/launches_list.html', context)

def home(request):
    next_launch = Launch.objects.filter(time__gt=datetime.now(pytz.utc)).last()
    last_launch = Launch.objects.filter(time__lte=datetime.now(pytz.utc)).first()
    
    # Gather all needed information to create next launch card
    if next_launch:
        next_launch_boosters = next_launch.get_boosters.replace("N/A", "Unknown")
        next_launch_recoveries = next_launch.get_recoveries
        next_launch_photo = PadUsed.objects.get(pad=next_launch.pad, rocket=next_launch.rocket).image.url
    else:
        next_launch_boosters = "TBD"
        next_launch_recoveries = "TBD"
        next_launch_photo = 'rocket_pad_photos/rocket_launch_image.jpg'

    next_launch_tugs = concatenated_list(list(Boat.objects.filter(type="TUG", tugonlaunch__launch=next_launch).all().values_list("name", flat=True)))
    next_launch_fairing_recovery = concatenated_list(list(set(Boat.objects.filter(type="FAIRING_RECOVERY", fairingrecovery__launch=next_launch).all().values_list("name", flat=True))))
    
    # Gather all needed information to create last launch card
    last_launch_boosters = last_launch.get_boosters
    last_launch_recoveries = last_launch.get_recoveries
    last_launch_photo = PadUsed.objects.get(pad=last_launch.pad, rocket=last_launch.rocket).image.url
    last_launch_tugs = concatenated_list(list(Boat.objects.filter(type="TUG", tugonlaunch__launch=last_launch).all().values_list("name", flat=True)))
    last_launch_fairing_recovery = concatenated_list(list(set(Boat.objects.filter(type="FAIRING_RECOVERY", fairingrecovery__launch=last_launch).all().values_list("name", flat=True))))
    
    # Gather information needed for all of the stats
    num_launches_per_rocket_and_successes = []
    for rocket in Rocket.objects.filter(provider__name="SpaceX"):
        num_launches_per_rocket_and_successes.append([rocket.name, rocket.num_launches, rocket.num_successes])

    num_landings_and_successes = get_landings_and_successes()
    most_flown_boosters = get_most_flown_boosters()
    most_flown_boosters_string = f"{concatenated_list(most_flown_boosters[0])}; {most_flown_boosters[1]} flights"
    quickest_booster_turnaround = last_launch.calculate_turnarounds(object=TurnaroundObjects.BOOSTER)
    quickest_booster_turnaround_string = f"{quickest_booster_turnaround['ordered_turnarounds'][0]['turnaround_object']} at {convert_seconds(quickest_booster_turnaround['ordered_turnarounds'][0]['turnaround_time'])}"
    shortest_time_between_launches = convert_seconds(last_launch.calculate_turnarounds(object=TurnaroundObjects.ALL)['ordered_turnarounds'][0]['turnaround_time'])
    
    # this section gets total number of reflights; it takes the number of booster uses and subtracts the number of boosters that have flown
    num_booster_uses = StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc)).filter(launch__rocket__name__icontains="Falcon").count()
    num_stages_used = Stage.objects.filter(type="BOOSTER", stageandrecovery__launch__time__lte=datetime.now(pytz.utc)).filter(rocket__name__icontains="Falcon").distinct().count()
    num_booster_reflights = num_booster_uses - num_stages_used

    falcon_9_reflights = Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Falcon 9").first().get_rocket_flights_reused_vehicle()
    falcon_heavy_reflights = Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket__name="Falcon Heavy").first().get_rocket_flights_reused_vehicle()

    pad_stats: list = []
    for pad in Pad.objects.filter(padused__rocket__provider__name="SpaceX").distinct().order_by("id"):
        num_landings = pad.num_launches
        fastest_turnaround = pad.fastest_turnaround
        pad_stats.append([pad, num_landings, fastest_turnaround])

    recovery_zone_stats: list = []
    for zone in LandingZone.objects.filter(stageandrecovery__stage__rocket__provider__name="SpaceX").distinct().order_by("id"):
        num_landings = zone.num_landings
        fastest_turnaround = zone.fastest_turnaround
        recovery_zone_stats.append([zone, num_landings, fastest_turnaround])

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
        'zone_stats': recovery_zone_stats,
        'shortest_time_between_launches': shortest_time_between_launches
    }
    return render(request, 'launches/home.html', context=context)

def launch_details(request, launch_name):
    launch = get_object_or_404(Launch, name=launch_name)
    context = {'data': launch.create_launch_table()}
    return render(request, 'launches/launch_table.html', context)
