from django.shortcuts import render, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.core.cache import cache
import urllib.parse
from django.db.models import Q
from booster_tracker.home_utils import (
    generate_home_page,
    generate_starship_home,
    generate_boosters_page,
    generate_spacecraft_list,
    get_model_objects_with_filter,
    launches_per_day,
    launch_turnaround_times,
    line_of_best_fit,
    launches_in_time_interval,
    get_next_and_last_launches,
    get_most_flown_stages,
    StageObjects,
)
from booster_tracker.utils import (
    concatenated_list,
    convert_seconds,
    TurnaroundObjects,
    make_monotonic,
    MonotonicDirections,
)

import pytz
import statistics
import numpy as np
from datetime import datetime

from booster_tracker.models import (
    Stage,
    StageAndRecovery,
    Launch,
    Spacecraft,
    SpacecraftOnLaunch,
    RocketFamily,
    SpacecraftFamily,
    Operator,
    Rocket,
    Orbit,
    Pad,
    LandingZone,
    Boat,
    FairingRecovery,
)

from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from booster_tracker.serializers import (
    LaunchSerializer,
    LaunchOnlySerializer,
    RocketOnlySerializer,
    RocketFamilySerializer,
    OperatorSerializer,
    OrbitSerializer,
    PadSerializer,
    LandingZoneSerializer,
    StageAndRecoverySerializer,
    LaunchInformationSerializer,
    StageSerializer,
    StageInformationSerializer,
    SpacecraftSerializer,
    SpacecraftInformationSerializer,
    BoatSerializer,
    SpacecraftFamilySerializer,
    HomePageSerializer,
    FamilyInformationSerializer,
)
import json


def launches_list(request):
    # Get the search query from the request
    query = request.GET.get("q")

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
    page_number = request.GET.get("page", 1)

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
        "paginated_launches": paginated_launches,
        "query": query,
    }

    return render(request, "launches/launches_list.html", context)


def home(request):
    cache_key = "home_page"
    cached_content = cache.get(cache_key)

    if cached_content:
        return render(request, "launches/home.html", cached_content)

    context = generate_home_page()
    cache.set(cache_key, context, timeout=None)

    return render(request, "launches/home.html", context)


def launch_details(request, encoded_launch_name):
    launch_name = urllib.parse.unquote(encoded_launch_name)
    launch = get_object_or_404(Launch, name=launch_name)
    context = {"data": launch.create_launch_table(), "launch": launch}
    return render(request, "launches/launch_table.html", context)


def stage_list(request, rocket_family_name: str, stage_type):
    rocket_family = RocketFamily.objects.get(name__icontains=rocket_family_name)
    cache_key = f"{rocket_family.name.lower()}_boosters"
    cached_content = cache.get(cache_key)

    if cached_content:
        return render(request, "stages/stage_list.html", cached_content)

    context = generate_boosters_page(rocket_family=rocket_family, stage_type=stage_type)
    cache.set(cache_key, context, timeout=None)

    return render(request, "stages/stage_list.html", context)


def stage_info(request, rocket_family: RocketFamily, stage_type, stage_name):
    stage = get_object_or_404(
        Stage,
        name=stage_name,
        rocket__name__icontains=rocket_family,
        type__icontains=stage_type,
    )
    launches = Launch.objects.filter(stageandrecovery__stage=stage).order_by("time")
    launches_information = []
    turnarounds = []

    for launch in launches:
        turnaround = launch.get_stage_flights_and_turnaround(stage=stage)[1]
        launches_information.append(
            [
                launch,
                turnaround,
                StageAndRecovery.objects.get(launch=launch, stage=stage),
            ]
        )
        if turnaround and launch.time < datetime.now(pytz.utc):
            turnarounds.append(turnaround)

    average_turnaround = None
    turnaround_stdev = None
    quickest_turnaround = None

    if len(turnarounds) > 0:
        average_turnaround = round(statistics.mean(turnarounds), 2)
        quickest_turnaround = round(min(turnarounds), 2)
    if len(turnarounds) > 1:
        turnaround_stdev = round(statistics.stdev(turnarounds), 2)

    context = {
        "stage": stage,
        "launches": launches_information,
        "average_turnaround": average_turnaround,
        "stdev": turnaround_stdev,
        "quickest_turnaround": quickest_turnaround,
    }

    return render(request, "stages/stage_info.html", context)


def dragon_list(request):
    cache_key = "Dragons"
    cached_content = cache.get(cache_key)

    if cached_content:
        return render(request, "dragons/dragon_list.html", cached_content)

    context = generate_spacecraft_list(SpacecraftFamily.objects.get(name="Dragon"))
    cache.set(cache_key, context, timeout=None)

    return render(request, "dragons/dragon_list.html", context)


def dragon_info(request, dragon_name):
    dragon = get_object_or_404(Spacecraft, name=dragon_name, family__name="Dragon")
    launches = Launch.objects.filter(spacecraftonlaunch__spacecraft=dragon).order_by("time")
    launches_information = []
    turnarounds = []

    for launch in launches:
        spacecraft_on_launch = SpacecraftOnLaunch.objects.get(launch=launch)
        turnaround = spacecraft_on_launch.get_turnaround()
        launches_information.append([launch, turnaround, spacecraft_on_launch])
        if turnaround and launch.time < datetime.now(pytz.utc):
            turnarounds.append(turnaround)

    average_turnaround = None
    turnaround_stdev = None
    quickest_turnaround = None

    if len(turnarounds) > 0:
        average_turnaround = round(statistics.mean(turnarounds), 2)
        quickest_turnaround = round(min(turnarounds), 2)
    if len(turnarounds) > 1:
        turnaround_stdev = round(statistics.stdev(turnarounds), 2)

    context = {
        "dragon": dragon,
        "launches": launches_information,
        "average_turnaround": average_turnaround,
        "stdev": turnaround_stdev,
        "quickest_turnaround": quickest_turnaround,
    }

    return render(request, "dragons/dragon_info.html", context)


def starship_home(request):
    cache_key = "starship_home"
    cached_content = cache.get(cache_key)

    if cached_content:
        return render(request, "starship/starship_home.html", cached_content)

    context = generate_starship_home()
    cache.set(cache_key, context, timeout=None)

    return render(request, "starship/starship_home.html", context)


def health(request):
    return HttpResponse("Success", status=200)


class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"


@api_view(["GET"])
def filter_launch_days(request):
    filter = json.loads(request.query_params.get("filter"))
    filtered_launches = get_model_objects_with_filter(Launch, filter)
    launches_on_day = launches_per_day(filtered_launches)

    num_days_with_launches = len(launches_on_day)
    percentage_days_with_launch = round(num_days_with_launches / 3.66, 2)

    max_launches = list(launches_on_day)[0][1]

    days_with_most_launches = []
    for day in launches_on_day:
        if day[1] == max_launches:
            days_with_most_launches.append(day[0])
        else:
            break

    return Response(
        {
            "numDaysWithLaunches": num_days_with_launches,
            "percentageDaysWithLaunches": percentage_days_with_launch,
            "mostLaunches": max_launches,
            "daysWithMostLaunches": concatenated_list(days_with_most_launches),
        }
    )


# This section handles the API view of the application:


class LaunchApiView(ListAPIView):
    serializer_class = LaunchSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        """Return the list of items for this view."""
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        filtered_launches = get_model_objects_with_filter(Launch, filter, query)
        return filtered_launches

    def get(self, request, *args, **kwargs):
        """List all the Launch items for given requested user"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OrbitApiView(APIView):
    def get(self, request, *args, **kwargs):
        orbits = Orbit.objects.all()
        serializer = OrbitSerializer(orbits, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LaunchOnlyApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List all the Launch items (without recoveries) for given requested user"""
        launches = Launch.objects.all()
        serializer = LaunchOnlySerializer(launches, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RocketApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List all the Rocket items for given requested user"""
        rockets = Rocket.objects.all()
        serializer = RocketOnlySerializer(rockets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RocketFamilyApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List all the RocketFamily items for given requested user"""
        rocketfamilies = RocketFamily.objects.all()
        serializer = RocketFamilySerializer(rocketfamilies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OperatorApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List all the Operator items for given requested user"""
        operators = Operator.objects.all()
        serializer = OperatorSerializer(operators, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PadApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List of all pads"""
        pads = Pad.objects.all()
        serializer = PadSerializer(pads, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandingZoneApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List of all landing zones"""
        zones = LandingZone.objects.all()
        serializer = LandingZoneSerializer(zones, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BoatApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List of all boats"""
        boats = Boat.objects.all()
        serializer = BoatSerializer(boats, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StageAndRecoveryApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List of all stage and recoveries"""
        stage_and_recoveries = StageAndRecovery.objects.all()
        serializer = StageAndRecoverySerializer(stage_and_recoveries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LaunchInformationApiView(RetrieveAPIView):
    serializer_class = LaunchInformationSerializer

    def get_object(self):
        """Get launch by ID"""
        id = self.request.query_params.get("id", "")
        return Launch.objects.get(id=id)


class StageApiView(ListAPIView):
    serializer_class = StageSerializer

    def get_queryset(self):
        """Return the list of items for this view."""
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        filtered_stages = get_model_objects_with_filter(Stage, filter, query).order_by("-name")
        return filtered_stages

    def get(self, request, *args, **kwargs):
        """List all the stage items for given requested user"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpacecraftFamilyApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List of all spacecraft families"""
        spacecraft_families = SpacecraftFamily.objects.all()
        serializer = SpacecraftFamilySerializer(spacecraft_families, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SpacecraftApiView(ListAPIView):
    serializer_class = SpacecraftSerializer

    def get_queryset(self):
        """Return the list of items for this view."""
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        filtered_spacecraft = get_model_objects_with_filter(Spacecraft, filter, query).order_by("-name")
        return filtered_spacecraft

    def get(self, request, *args, **kwargs):
        """List all the spacecraft items for given requested user"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StageInformationApiView(RetrieveAPIView):
    serializer_class = StageInformationSerializer

    def get_object(self):
        """Get stage by ID"""
        id = self.request.query_params.get("id", "")
        return Stage.objects.get(id=id)


class SpacecraftInformationApiView(RetrieveAPIView):
    serializer_class = SpacecraftInformationSerializer

    def get_object(self):
        """Get spacecraft by ID"""
        id = self.request.query_params.get("id", "")
        return Spacecraft.objects.get(id=id)


class HomeDataApiView(APIView):
    def get(self, request):
        print(datetime.now(), "func start")
        date_str = self.request.query_params.get("startdate", "").strip('"').replace("Z", "")
        start_time = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=pytz.utc)
        today = datetime.now(pytz.utc)
        function_type = self.request.query_params.get("functiontype", "")

        # Temporary filter, will be sent from API
        received_filter = {}
        # Get filtered launches, filtering by time
        filtered_launches = (
            get_model_objects_with_filter(Launch, filter=received_filter)
            .filter(time__gte=start_time, time__lte=today)
            .order_by("time")
        )

        turnaround_data = launch_turnaround_times(filtered_launches=filtered_launches)
        turnaround_values = list(turnaround_data.values())
        chunk_size = 10

        # Create x_values based on chunk_size
        x_values = list(range(0, len(turnaround_values), chunk_size // 2))

        # Calculate the best fit line for all x values
        weights = np.linspace(1, 1.1, len(turnaround_values))  # Increasing weights
        all_x_values = list(range(len(turnaround_values)))
        best_fit_line = line_of_best_fit(x=all_x_values, y=turnaround_values, fit_type=function_type, weights=weights)

        # Calculate the best fit values for all x values
        best_fit_turnaround_values = [best_fit_line(x) for x in x_values]

        # Insert null values at every other x value in turnaround_values; this is to break values up on line chart
        averaged_values = [(turnaround_values[x] if i % 2 == 0 else None) for i, x in enumerate(x_values)]

        # Calculate current launch number (the last one in the list)
        current_launch_number = len(filtered_launches)

        # Calculate remaining launches for the current year
        days_in_current_year = 366 if today.year % 4 == 0 else 365
        days_passed_current_year = (today - datetime(today.year, 1, 1, tzinfo=pytz.utc)).days
        remaining_days_current_year = days_in_current_year - days_passed_current_year

        launches_this_year = filtered_launches.filter(time__gte=(datetime(today.year, 1, 1, tzinfo=pytz.utc))).count()

        remaining_launches_current_year = (
            launches_in_time_interval(
                line_of_best_fit=best_fit_line,
                start_launch_num=current_launch_number,
                remaining_days=remaining_days_current_year,
                min_value=0.33,
            )
            - current_launch_number
        )

        # Calculate total launches for the next year
        next_year_days = 366 if (today.year + 1) % 4 == 0 else 365
        next_year_launches = launches_in_time_interval(
            line_of_best_fit=best_fit_line,
            start_launch_num=current_launch_number + remaining_launches_current_year,
            remaining_days=next_year_days,
            min_value=0.33,
        )

        # Calculate total launches for the year after next
        year_after_next_days = 366 if (today.year + 2) % 4 == 0 else 365
        year_after_next_launches = launches_in_time_interval(
            line_of_best_fit=best_fit_line,
            start_launch_num=next_year_launches,
            remaining_days=year_after_next_days,
            min_value=0.33,
        )

        # Get homepage stats
        next_launch, last_launch = get_next_and_last_launches()
        num_missions = Launch.objects.filter(rocket__family__provider__name="SpaceX").count()
        num_successes = Launch.objects.filter(rocket__family__provider__name="SpaceX", launch_outcome="SUCCESS").count()
        num_landings = (
            StageAndRecovery.objects.filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
            .filter(method_success="SUCCESS")
            .count()
        )
        shortest_time_between_launches = convert_seconds(
            last_launch.calculate_turnarounds(turnaround_object=TurnaroundObjects.ALL)["ordered_turnarounds"][0][
                "turnaround_time"
            ]
        )

        num_stage_uses = (
            StageAndRecovery.objects.filter(launch__time__lte=datetime.now(pytz.utc))
            .filter(launch__rocket__name__icontains="Falcon")
            .count()
        )
        num_stages_used = (
            Stage.objects.filter(stageandrecovery__launch__time__lte=datetime.now(pytz.utc))
            .filter(rocket__family__provider__name="SpaceX")
            .distinct()
            .count()
        )
        num_stage_reflights = num_stage_uses - num_stages_used

        # Prepare data for serialization
        data = {
            "turnaround_x_values": x_values,
            "turnaround_data": averaged_values,
            "best_fit_turnaround_values": best_fit_turnaround_values,
            "remaining_launches_current_year": remaining_launches_current_year,
            "total_launches_current_year": launches_this_year + remaining_launches_current_year,
            "total_launches_next_year": next_year_launches - (current_launch_number + remaining_launches_current_year),
            "total_launches_year_after_next": year_after_next_launches - next_year_launches,
            "next_launch": next_launch,
            "last_launch": last_launch,
            "num_missions": num_missions,
            "num_successes": num_successes,
            "num_landings": num_landings,
            "shortest_time_between_launches": shortest_time_between_launches,
            "num_stage_reflights": num_stage_reflights,
        }

        # Serialize data
        serializer = HomePageSerializer(data)

        # Return serialized data in response
        print(datetime.now(), "func end")
        return Response(serializer.data)


class FamilyInformationApiView(APIView):
    def get(self, request):
        family = RocketFamily.objects.get(name="Falcon")
        stage_type = StageObjects.BOOSTER

        # Determine the first launch year and the current year
        first_launch_year = Launch.objects.filter(rocket__family__name=family).order_by("time").first().time.year
        current_year = datetime.now(pytz.utc).year

        # Initialize dictionaries and lists to store flight data
        max_reflight_num = {}
        avg_reflight_num = []
        max_fairing_flights = []

        # Loop through each year from the first launch to the current year
        for year in range(first_launch_year, current_year + 1):
            if year == current_year:
                before_date = datetime.now(pytz.utc)
            else:
                before_date = datetime(year, 12, 31, 23, 59, 59, 999, tzinfo=pytz.utc)

            # Get stage data for the specified year
            stage_data = get_most_flown_stages(
                family=family,
                stage_type=stage_type,
                before_date=before_date,
            )
            max_reflight_num[year] = stage_data["num_launches"]

            # Initialize list to store booster flight numbers for the year
            booster_flight_nums = []

            # Collect booster flight numbers for all launches in the year
            for launch in Launch.objects.filter(
                time__gte=datetime(year, 1, 1, 0, 0, tzinfo=pytz.utc), time__lte=before_date
            ).all():
                for stageandrecovery in StageAndRecovery.objects.filter(launch=launch):
                    booster_flight_nums.append(stageandrecovery.num_flights)

            # Calculate average booster reflights for the year
            avg_reflight_num.append(statistics.mean(booster_flight_nums) if booster_flight_nums else 0)

            # Determine the maximum fairing flights for the year
            max_num = 0
            for fairing_recovery in FairingRecovery.objects.filter(launch__time__lte=before_date).all():
                if fairing_recovery.flights not in ["Unknown", ""]:
                    if int(fairing_recovery.flights) > max_num:
                        max_num = int(fairing_recovery.flights)
            max_fairing_flights.append(max_num)

        # Initialize dictionary to store family statistics
        family_stats = {}

        # Calculate total number of missions and successful landings for the family
        num_missions = Launch.objects.filter(rocket__family__name=family).count()
        num_landings = StageAndRecovery.objects.filter(
            launch__rocket__family__name=family,
            method__in=["DRONE_SHIP", "GROUND_PAD", "CATCH"],
            method_success="SUCCESS",
        ).count()

        # Store mission and landing data in the family stats dictionary
        family_stats["Missions"] = str(num_missions)
        family_stats["Landings"] = str(num_landings)
        family_stats["Reuses"] = str(
            StageAndRecovery.objects.filter(launch__rocket__family__name=family, num_flights__gt=1).count()
        )

        # Initialize dictionary to store statistics for each rocket in the family
        family_children_stats = {}

        # Collect data for each rocket in the family
        for rocket in Rocket.objects.filter(family__name=family):
            last_launch: Launch = (
                Launch.objects.filter(time__lte=datetime.now(pytz.utc), rocket=rocket).order_by("-time").first()
            )
            booster_reflights = StageAndRecovery.objects.filter(
                launch__rocket__name=rocket.name, num_flights__gt=1, stage__type=StageObjects.BOOSTER
            ).count()
            stage_two_reflights = StageAndRecovery.objects.filter(
                launch__rocket__name=rocket.name, num_flights__gt=1, stage__type=StageObjects.SECOND_STAGE
            ).count()
            launches = Launch.objects.filter(rocket=rocket).count()
            successes = Launch.objects.filter(rocket=rocket, launch_outcome="SUCCESS").count()
            flight_proven_launches = last_launch.get_rocket_flights_reused_vehicle()

            # Store data in the family children stats dictionary
            family_children_stats[rocket.name] = {
                "Launches": str(launches),
                "Successes": str(successes),
                "Booster Reflights": str(booster_reflights),
                "2nd Stage Reflights": str(stage_two_reflights),
                "Flight Proven Launches": str(flight_proven_launches),
            }

        # Gather list of most stage stats:
        booster_most_flight_stats = get_most_flown_stages(
            family=family, stage_type=StageObjects.BOOSTER, before_date=datetime.now(pytz.utc)
        )
        boosters_with_most_flights = booster_most_flight_stats["stages"]
        booster_max_num_flights = booster_most_flight_stats["num_launches"]

        stage_two_most_flight_stats = get_most_flown_stages(
            family=family, stage_type=StageObjects.SECOND_STAGE, before_date=datetime.now(pytz.utc)
        )
        stage_two_with_most_flights = stage_two_most_flight_stats["stages"]
        stage_two_max_num_flights = stage_two_most_flight_stats["num_launches"]

        quickest_booster_stage_and_recovery = (
            StageAndRecovery.objects.filter(
                stage__rocket__family=family, stage__type="BOOSTER", launch__time__lte=datetime.now(pytz.utc)
            )
            .order_by("stage_turnaround")
            .first()
        )
        if quickest_booster_stage_and_recovery:
            booster_with_quickest_turnaround = quickest_booster_stage_and_recovery.stage
            booster_turnaround_time = convert_seconds(quickest_booster_stage_and_recovery.stage_turnaround)
        else:
            booster_with_quickest_turnaround = None
            booster_turnaround_time = None

        quickest_stage_two_stage_and_recovery = (
            StageAndRecovery.objects.filter(
                stage__rocket__family=family, stage__type="SECOND_STAGE", launch__time__lte=datetime.now(pytz.utc)
            )
            .order_by("stage_turnaround")
            .first()
        )
        if quickest_stage_two_stage_and_recovery:
            stage_two_with_quickest_turnaround = quickest_stage_two_stage_and_recovery.stage
            stage_two_turnaround_time = convert_seconds(quickest_stage_two_stage_and_recovery.stage_turnaround)
        else:
            stage_two_with_quickest_turnaround = None
            stage_two_turnaround_time = None

        # Compile all collected data into a single dictionary
        data = {
            "max_reflight_num": max_reflight_num,
            "avg_reflight_num": avg_reflight_num,
            "max_fairing_flights": max_fairing_flights,
            "stats": family_stats,
            "children_stats": family_children_stats,
            "boosters_with_most_flights": boosters_with_most_flights,
            "booster_max_num_flights": booster_max_num_flights,
            "stage_two_with_most_flights": stage_two_with_most_flights,
            "stage_two_max_num_flights": stage_two_max_num_flights,
            "booster_with_quickest_turnaround": booster_with_quickest_turnaround,
            "booster_turnaround_time": booster_turnaround_time,
            "stage_two_with_quickest_turnaround": stage_two_with_quickest_turnaround,
            "stage_two_turnaround_time": stage_two_turnaround_time,
        }

        # Serialize the data
        serializer = FamilyInformationSerializer(data)

        # Return the serialized data as a response
        return Response(serializer.data)
