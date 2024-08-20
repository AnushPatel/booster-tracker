from django.db.models import Q, Count, Max, Avg
from django.db.models.functions import ExtractYear
from booster_tracker.home_utils import (
    get_model_objects_with_filter,
    launches_per_day,
    launch_turnaround_times,
    line_of_best_fit,
    launches_in_time_interval,
    get_next_and_last_launches,
    get_most_flown_stages,
    StageObjects,
    build_filter,
)
from booster_tracker.utils import (
    concatenated_list,
    convert_seconds,
    TurnaroundObjects,
    all_zeros,
    parse_start_time,
    get_start_date,
)
from rest_framework.pagination import PageNumberPagination
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
    PadInformationSerializer,
    LandingZoneSerializer,
    LandingZoneInformationSerializer,
    StageAndRecoverySerializer,
    LaunchInformationSerializer,
    StageInformationSerializer,
    SpacecraftListSerializer,
    SpacecraftInformationSerializer,
    BoatSerializer,
    SpacecraftFamilySerializer,
    HomePageSerializer,
    FamilyInformationSerializer,
    CalendarStatsSerializer,
    StageListSerializer,
)
import json


class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"


# APIViews without any additional logic
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


class SpacecraftFamilyApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List of all spacecraft families"""
        spacecraft_families = SpacecraftFamily.objects.all()
        serializer = SpacecraftFamilySerializer(spacecraft_families, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Launch Calendar Stats
class FilteredLaunchDaysApiView(APIView):
    def get(self, request):
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

        data = {
            "numDaysWithLaunches": num_days_with_launches,
            "percentageDaysWithLaunches": percentage_days_with_launch,
            "mostLaunches": max_launches,
            "daysWithMostLaunches": concatenated_list(days_with_most_launches),
            "launches": filtered_launches,
        }

        serializer = CalendarStatsSerializer(data)

        return Response(serializer.data)


# List API views


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


class PadApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List of all pads"""
        filter_param = self.request.query_params.get("filter", "{}")

        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        filtered_pads = get_model_objects_with_filter(Pad, filter, query).order_by("-name")
        serializer = PadSerializer(filtered_pads, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LandingZoneApiView(APIView):
    def get(self, request, *args, **kwargs):
        """List of all landing zones"""
        filter_param = self.request.query_params.get("filter", "{}")

        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        filtered_zones = get_model_objects_with_filter(LandingZone, filter, query).order_by("-name")
        serializer = LandingZoneSerializer(filtered_zones, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StageApiView(APIView):
    def get(self, request, *args, **kwargs):
        # Get information from URL
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        type = self.request.query_params.get("type")
        query = self.request.query_params.get("query", "")
        family_str = self.request.query_params.get("family", "")
        family = RocketFamily.objects.get(name__icontains=family_str)

        # Prepare information
        start_filter = build_filter(model=Stage, family=family, type=type)
        filtered_stages = (
            get_model_objects_with_filter(Stage, filter, query)
            .filter(type=type, rocket__family=family)
            .order_by("-version", "-name")
        )

        data = {"start_filter": start_filter, "stages": filtered_stages}

        serializer = StageListSerializer(data)

        return Response(serializer.data)


class SpacecraftApiView(ListAPIView):
    def get(self, request, *args, **kwargs):
        # Get information from URL
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        family_str = self.request.query_params.get("family", "")
        family = SpacecraftFamily.objects.get(name__icontains=family_str)

        # Prepare information
        start_filter = build_filter(model=Spacecraft, family=family, type=None)
        filtered_spacecraft = (
            get_model_objects_with_filter(Spacecraft, filter, query).filter(family=family).order_by("-name")
        )

        data = {"start_filter": start_filter, "spacecraft": filtered_spacecraft}

        serializer = SpacecraftListSerializer(data)

        return Response(serializer.data)


# Information API Views


class LaunchInformationApiView(RetrieveAPIView):
    serializer_class = LaunchInformationSerializer

    def get_object(self):
        """Get launch by ID"""
        id = self.request.query_params.get("id", "")
        return Launch.objects.get(id=id)


class LandingZoneInformationApiView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        """Get stage by ID"""
        id = self.request.query_params.get("id", "")
        landing_zone = LandingZone.objects.get(id=id)
        filtered_stage_and_recoveries = StageAndRecovery.objects.filter(landing_zone=landing_zone).order_by(
            "launch__time"
        )
        display_items = filtered_stage_and_recoveries.filter(launch__time__lte=datetime.now(pytz.utc)).reverse()[:25]

        start_date = get_start_date(filtered_stage_and_recoveries.first())
        start_time = parse_start_time(self.request.query_params, start_date)

        stage_and_recoveries = filtered_stage_and_recoveries.filter(launch__time__gte=start_time)

        data = {
            "landing_zone": landing_zone,
            "stage_and_recoveries": stage_and_recoveries,
            "display_stage_and_recoveries": display_items,
            "start_date": start_date,
        }

        serializer = LandingZoneInformationSerializer(data)

        return Response(serializer.data)


class StageInformationApiView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        """Get stage by ID"""
        id = self.request.query_params.get("id", "")
        stage = Stage.objects.get(id=id)
        filtered_stage_and_recoveries = StageAndRecovery.objects.filter(stage=stage).order_by("launch__time")
        display_items = filtered_stage_and_recoveries.filter(launch__time__lte=datetime.now(pytz.utc)).reverse()

        start_date = get_start_date(filtered_stage_and_recoveries.first())
        start_time = parse_start_time(self.request.query_params, start_date)

        stage_and_recoveries = filtered_stage_and_recoveries.filter(launch__time__gte=start_time)

        data = {
            "stage": stage,
            "stage_and_recoveries": stage_and_recoveries,
            "display_stage_and_recoveries": display_items,
            "start_date": start_date,
        }

        serializer = StageInformationSerializer(data)

        return Response(serializer.data)


class SpacecraftInformationApiView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        """Get spacecraft by ID"""
        id = self.request.query_params.get("id", "")
        spacecraft = Spacecraft.objects.get(id=id)
        filtered_spacecraft_on_launch = SpacecraftOnLaunch.objects.filter(spacecraft=spacecraft).order_by(
            "launch__time"
        )
        display_items = filtered_spacecraft_on_launch.filter(launch__time__lte=datetime.now(pytz.utc)).reverse()

        start_date = get_start_date(filtered_spacecraft_on_launch.first())
        start_time = parse_start_time(self.request.query_params, start_date)

        spacecraft_on_launches = filtered_spacecraft_on_launch.filter(launch__time__gte=start_time)

        data = {
            "spacecraft": spacecraft,
            "spacecraft_on_launches": spacecraft_on_launches,
            "display_spacecraft_on_launches": display_items,
            "start_date": start_date,
        }

        serializer = SpacecraftInformationSerializer(data)

        return Response(serializer.data)


class PadInformationApiView(RetrieveAPIView):
    def get(self, request, *args, **kwargs):
        """Get pad by ID"""
        id = self.request.query_params.get("id", "")
        pad = Pad.objects.get(id=id)
        filtered_launches = Launch.objects.filter(pad=pad).order_by("time")
        display_launches = filtered_launches.filter(time__lte=datetime.now(pytz.utc)).reverse()[:25]

        start_date = get_start_date(filtered_launches.first())
        start_time = parse_start_time(self.request.query_params, start_date)

        launches = filtered_launches.filter(time__gte=start_time)

        data = {
            "pad": pad,
            "launches": launches,
            "display_launches": display_launches,
            "start_date": start_date,
        }

        serializer = PadInformationSerializer(data)

        return Response(serializer.data)


# API views for home and rocket families


class HomeDataApiView(APIView):
    def get(self, request):
        today = datetime.now(pytz.utc)
        start_time = parse_start_time(self.request.query_params, today)
        function_type = self.request.query_params.get("functiontype", "")

        # Get launches per rocket per year:
        launches_per_rocket_per_year, years = self._get_launches_per_vehicle_per_year()

        # Get filtered launches
        filtered_launches = (
            get_model_objects_with_filter(Launch, filter={}, search_query="")
            .filter(time__gte=start_time, time__lte=today)
            .order_by("time")
        )

        # Fetch basic stats
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
        num_stage_reflights = self._calculate_num_stage_reflights()

        if not filtered_launches.exists():
            data = self._prepare_empty_response_data(
                next_launch,
                last_launch,
                num_missions,
                num_successes,
                num_landings,
                shortest_time_between_launches,
                num_stage_reflights,
                years,
                launches_per_rocket_per_year,
            )
            serializer = HomePageSerializer(data)
            return Response(serializer.data)

        # Process turnaround data and best fit calculations
        turnaround_data = self._process_turnaround_data(filtered_launches, function_type)

        # Calculate future launch predictions
        launch_predictions = self._calculate_launch_predictions(
            filtered_launches, today, turnaround_data["best_fit_line"]
        )

        data = {
            "turnaround_x_values": turnaround_data["x_values"],
            "turnaround_data": turnaround_data["averaged_values"],
            "best_fit_turnaround_values": turnaround_data["best_fit_turnaround_values"],
            "total_launches_current_year": launch_predictions["total_launches_current_year"],
            "total_launches_next_year": launch_predictions["total_launches_next_year"],
            "total_launches_year_after_next": launch_predictions["total_launches_year_after_next"],
            "next_launch": next_launch,
            "last_launch": last_launch,
            "num_missions": num_missions,
            "num_successes": num_successes,
            "num_landings": num_landings,
            "shortest_time_between_launches": shortest_time_between_launches,
            "num_stage_reflights": num_stage_reflights,
            "years": years,
            "launches_per_rocket_per_year": launches_per_rocket_per_year,
        }

        serializer = HomePageSerializer(data)
        return Response(serializer.data)

    def _prepare_empty_response_data(
        self,
        next_launch,
        last_launch,
        num_missions,
        num_successes,
        num_landings,
        shortest_time_between_launches,
        num_stage_reflights,
        years,
        launches_per_rocket_per_year,
    ):
        return {
            "turnaround_x_values": [],
            "turnaround_data": [],
            "best_fit_turnaround_values": [],
            "remaining_launches_current_year": 0,
            "total_launches_current_year": 0,
            "total_launches_next_year": 0,
            "total_launches_year_after_next": 0,
            "next_launch": next_launch,
            "last_launch": last_launch,
            "num_missions": num_missions,
            "num_successes": num_successes,
            "num_landings": num_landings,
            "shortest_time_between_launches": shortest_time_between_launches,
            "num_stage_reflights": num_stage_reflights,
            "years": years,
            "launches_per_rocket_per_year": launches_per_rocket_per_year,
        }

    def _get_launches_per_vehicle_per_year(self):
        launches_per_rocket_per_year = {}
        current_year = datetime.now().year

        # Initialize a variable to track the global minimum year
        global_min_year = current_year

        # First pass: Find the global minimum year across all rockets
        for rocket in Rocket.objects.filter(family__provider__name="SpaceX"):
            launches_per_year = (
                Launch.objects.filter(rocket=rocket)
                .annotate(year=ExtractYear("time"))
                .values("year")
                .annotate(count=Count("id"))
                .order_by("year")
            )

            if launches_per_year.exists():
                rocket_min_year = min(entry["year"] for entry in launches_per_year)
                global_min_year = min(global_min_year, rocket_min_year)

        # Second pass: Populate the dictionary with zeros for missing years
        for rocket in Rocket.objects.filter(family__provider__name="SpaceX").order_by("-name"):
            launches_per_year = (
                Launch.objects.filter(rocket=rocket)
                .annotate(year=ExtractYear("time"))
                .values("year")
                .annotate(count=Count("id"))
                .order_by("year")
            )

            # Convert the queryset to a dictionary
            formatted_dict = {entry["year"]: entry["count"] for entry in launches_per_year}

            # Fill in missing years with zeros from global_min_year to current_year
            for year in range(global_min_year, current_year + 1):
                if year not in formatted_dict:
                    formatted_dict[year] = 0

            # Sort the dictionary by year
            launches_per_rocket_per_year[rocket.id] = list(dict(sorted(formatted_dict.items())).values())
            years = list(formatted_dict.keys())

        return launches_per_rocket_per_year, years

    def _calculate_num_stage_reflights(self):
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
        return num_stage_uses - num_stages_used

    def _process_turnaround_data(self, filtered_launches, function_type):
        turnaround_data = launch_turnaround_times(filtered_launches=filtered_launches)
        turnaround_values = list(turnaround_data.values())
        chunk_size = 10

        x_values = list(range(0, len(turnaround_values), chunk_size // 2))
        all_x_values = list(range(len(turnaround_values)))
        # Get all spacex launches
        all_spacex_launches = Launch.objects.filter(rocket__family__provider__name="SpaceX").order_by("-time")

        # Determine the count of launches and calculate the top 10%
        launch_count = all_spacex_launches.count()
        recent_10_percent_count = max(1, int(launch_count * 0.10))

        # Slice the queryset to get the most recent 10% and calculate the average
        recent_average = (
            all_spacex_launches[:recent_10_percent_count].aggregate(Avg("company_turnaround"))[
                "company_turnaround__avg"
            ]
            / 86400
        )
        print(recent_average)
        best_fit_line = line_of_best_fit(
            x=all_x_values,
            y=turnaround_values,
            fit_type=function_type,
            weights=None,
            long_term_behavior_max=recent_average / 2,
        )

        best_fit_turnaround_values = [best_fit_line(x) for x in x_values]
        averaged_values = [(turnaround_values[x] if i % 2 == 0 else None) for i, x in enumerate(x_values)]

        return {
            "turnaround_data": turnaround_data,
            "best_fit_turnaround_values": best_fit_turnaround_values,
            "x_values": x_values,
            "averaged_values": averaged_values,
            "best_fit_line": best_fit_line,
        }

    def _calculate_launch_predictions(self, filtered_launches, today, best_fit_line):
        current_launch_number = len(filtered_launches)
        days_in_current_year = 366 if today.year % 4 == 0 else 365
        days_passed_current_year = (today - datetime(today.year, 1, 1, tzinfo=pytz.utc)).days
        remaining_days_current_year = days_in_current_year - days_passed_current_year

        launches_this_year = filtered_launches.filter(time__gte=(datetime(today.year, 1, 1, tzinfo=pytz.utc))).count()

        # Calculate the remaining launches for the current year
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

        return {
            "total_launches_current_year": remaining_launches_current_year + launches_this_year,
            "total_launches_next_year": next_year_launches - (current_launch_number + remaining_launches_current_year),
            "total_launches_year_after_next": year_after_next_launches - next_year_launches,
        }


class FamilyInformationApiView(APIView):
    def get(self, request):
        print("start", datetime.now())
        family = self._get_rocket_family()
        first_launch_time = Launch.objects.filter(rocket__family=family).order_by("time").first().time
        start_year, current_year = self._get_launch_years(family)
        (
            max_booster_flights,
            avg_booster_flights,
            max_fairing_flights,
            max_stage_two_flights,
            avg_stage_two_flights,
            x_axis,
        ) = self._get_flight_data(family, start_year, current_year)
        family_stats = self._get_family_stats(family)
        family_children_stats = self._get_family_children_stats(family)
        (
            boosters_with_most_flights,
            stage_two_with_most_flights,
            booster_with_quickest_turnaround,
            booster_turnaround_time,
            stage_two_with_quickest_turnaround,
            stage_two_turnaround_time,
        ) = self._get_stage_stats(family)
        series_data = self._get_series_data(
            max_booster_flights, avg_booster_flights, max_fairing_flights, max_stage_two_flights, avg_stage_two_flights
        )

        # Compile all collected data into a single dictionary
        data = {
            "launch_years": x_axis,
            "series_data": series_data,
            "stats": family_stats,
            "children_stats": family_children_stats,
            "boosters_with_most_flights": boosters_with_most_flights,
            "stage_two_with_most_flights": stage_two_with_most_flights,
            "booster_with_quickest_turnaround": booster_with_quickest_turnaround,
            "booster_turnaround_time": booster_turnaround_time,
            "stage_two_with_quickest_turnaround": stage_two_with_quickest_turnaround,
            "stage_two_turnaround_time": stage_two_turnaround_time,
            "start_date": first_launch_time,
        }

        # Serialize the data
        serializer = FamilyInformationSerializer(data)

        # Return the serialized data as a response
        print("end", datetime.now())
        return Response(serializer.data)

    def _get_rocket_family(self):
        return RocketFamily.objects.get(name__icontains=self.request.query_params.get("family", ""))

    def _get_launch_years(self, family):
        first_launch_year = Launch.objects.filter(rocket__family=family).order_by("time").first().time
        current_year = datetime.now(pytz.utc).year

        start_year = parse_start_time(self.request.query_params, first_launch_year).year

        return start_year, current_year

    def _get_flight_data(self, family, start_year, current_year):
        # Create a list of years in the range
        x_axis = list(range(start_year, current_year + 1))

        # Create a single queryset for all necessary data, grouped by year
        flight_data = (
            StageAndRecovery.objects.filter(
                stage__rocket__family=family,
                launch__time__year__gte=start_year,
                launch__time__lte=datetime.now(pytz.utc),
            )
            .annotate(year=ExtractYear("launch__time"))
            .values("year", "stage__type")
            .annotate(
                max_flights=Max("num_flights"),
                avg_flights=Avg("num_flights"),
            )
            .order_by("year", "stage__type")
        )

        fairing_flight_data = (
            FairingRecovery.objects.filter(
                launch__rocket__family=family,
                launch__time__year__gte=start_year,
                launch__time__lte=datetime.now(pytz.utc),
            )
            .annotate(year=ExtractYear("launch__time"))
            .values("year")
            .annotate(
                max_flights=Max("flights"),
            )
            .order_by("year")
        )

        # Initialize dictionaries to hold the max and avg flights for each stage type by year
        max_booster_flights = {year: 0 for year in x_axis}
        avg_booster_flights = {year: 0 for year in x_axis}
        max_stage_two_flights = {year: 0 for year in x_axis}
        avg_stage_two_flights = {year: 0 for year in x_axis}
        max_fairing_flights = {year: 0 for year in x_axis}

        # Populate stage data from query set
        for data in flight_data:
            year = data["year"]
            stage_type = data["stage__type"]
            if stage_type == StageObjects.BOOSTER:
                max_booster_flights[year] = data["max_flights"]
                avg_booster_flights[year] = round(data["avg_flights"], 2)
            elif stage_type == StageObjects.SECOND_STAGE:
                max_stage_two_flights[year] = data["max_flights"]
                avg_stage_two_flights[year] = round(data["avg_flights"], 2)

        # Populate fairing data from query set
        for data in fairing_flight_data:
            year = data["year"]
            max_fairing_flights[year] = data["max_flights"]

        # Convert dictionaries to lists for return
        max_booster_flights = max_booster_flights.values()
        avg_booster_flights = avg_booster_flights.values()
        max_stage_two_flights = max_stage_two_flights.values()
        avg_stage_two_flights = avg_stage_two_flights.values()
        max_fairing_flights = max_fairing_flights.values()

        return (
            max_booster_flights,
            avg_booster_flights,
            max_fairing_flights,
            max_stage_two_flights,
            avg_stage_two_flights,
            x_axis,
        )

    def _get_stage_data(self, family, stage_type, before_date):
        stage_data = get_most_flown_stages(family=family, stage_type=stage_type, before_date=before_date)
        return stage_data["num_launches"]

    def _get_flight_numbers(self, family, year, before_date):
        booster_flight_nums = []
        stage_two_flight_nums = []

        for stageandrecovery in StageAndRecovery.objects.filter(
            launch__time__gte=datetime(year, 1, 1, 0, 0, tzinfo=pytz.utc),
            launch__time__lte=before_date,
            stage__rocket__family=family,
        ).all():
            if stageandrecovery.stage.type == StageObjects.BOOSTER:
                booster_flight_nums.append(stageandrecovery.num_flights)
            elif stageandrecovery.stage.type == StageObjects.SECOND_STAGE:
                stage_two_flight_nums.append(stageandrecovery.num_flights)

        return booster_flight_nums, stage_two_flight_nums

    def _get_max_fairing_flights(self, family, before_date):
        max_num = 0
        for fairing_recovery in FairingRecovery.objects.filter(
            launch__time__lte=before_date, launch__rocket__family=family
        ).all():
            if fairing_recovery.flights not in ["Unknown", ""]:
                max_num = max(max_num, int(fairing_recovery.flights))
        return max_num

    def _get_family_stats(self, family):
        num_missions = Launch.objects.filter(rocket__family__name=family).count()
        num_landings = StageAndRecovery.objects.filter(
            launch__rocket__family__name=family,
            method__in=["DRONE_SHIP", "GROUND_PAD", "CATCH"],
            method_success="SUCCESS",
        ).count()

        family_stats = {
            "Missions": str(num_missions),
            "Landings": str(num_landings),
            "Reuses": str(
                StageAndRecovery.objects.filter(launch__rocket__family__name=family, num_flights__gt=1).count()
            ),
        }
        return family_stats

    def _get_family_children_stats(self, family):
        family_children_stats = {}

        for rocket in Rocket.objects.filter(family__name=family).order_by("id"):
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

            family_children_stats[rocket.name] = {
                "Launches": str(launches),
                "Successes": str(successes),
                "Booster Reflights": str(booster_reflights),
                "2nd Stage Reflights": str(stage_two_reflights),
                "Flight Proven Launches": str(flight_proven_launches),
            }

        return family_children_stats

    def _get_stage_stats(self, family):
        booster_most_flight_stats = get_most_flown_stages(
            family=family, stage_type=StageObjects.BOOSTER, before_date=datetime.now(pytz.utc)
        )
        stage_two_most_flight_stats = get_most_flown_stages(
            family=family, stage_type=StageObjects.SECOND_STAGE, before_date=datetime.now(pytz.utc)
        )

        quickest_booster_stage_and_recovery = (
            StageAndRecovery.objects.filter(
                stage__rocket__family=family, stage__type="BOOSTER", launch__time__lte=datetime.now(pytz.utc)
            )
            .exclude(stage_turnaround__isnull=True)
            .order_by("stage_turnaround")
            .first()
        )
        quickest_stage_two_stage_and_recovery = (
            StageAndRecovery.objects.filter(
                stage__rocket__family=family, stage__type="SECOND_STAGE", launch__time__lte=datetime.now(pytz.utc)
            )
            .exclude(stage_turnaround__isnull=True)
            .order_by("stage_turnaround")
            .first()
        )

        if quickest_booster_stage_and_recovery:
            booster_with_quickest_turnaround = quickest_booster_stage_and_recovery.stage
            booster_turnaround_time = convert_seconds(quickest_booster_stage_and_recovery.stage_turnaround)
        else:
            booster_with_quickest_turnaround = None
            booster_turnaround_time = None

        if quickest_stage_two_stage_and_recovery:
            stage_two_with_quickest_turnaround = quickest_stage_two_stage_and_recovery.stage
            stage_two_turnaround_time = convert_seconds(quickest_stage_two_stage_and_recovery.stage_turnaround)
        else:
            stage_two_with_quickest_turnaround = None
            stage_two_turnaround_time = None

        return (
            booster_most_flight_stats["stages"],
            stage_two_most_flight_stats["stages"],
            booster_with_quickest_turnaround,
            booster_turnaround_time,
            stage_two_with_quickest_turnaround,
            stage_two_turnaround_time,
        )

    def _get_series_data(
        self,
        max_booster_flights,
        avg_booster_flights,
        max_fairing_flights,
        max_stage_two_flights,
        avg_stage_two_flights,
    ):
        series_data = {
            "Max Booster": max_booster_flights,
            "Avg Booster": avg_booster_flights,
            "Max Fairing": max_fairing_flights,
            "Max Stage 2": max_stage_two_flights,
            "Avg Stage 2": avg_stage_two_flights,
        }

        # Filter out entries where all values are zero
        filtered_series_data = {k: v for k, v in series_data.items() if not all_zeros(v)}

        return filtered_series_data
