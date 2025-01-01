from django.db.models import (
    Q,
    Count,
    Max,
    Avg,
    Sum,
    Value,
    FloatField,
    Case,
    When,
    Count,
    F,
    ExpressionWrapper,
    DurationField,
)
from django.db.models.functions import Cast
from django.db.models.functions import ExtractYear, Coalesce
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from booster_tracker.home_utils import (
    get_model_objects_with_filter,
    launches_per_day,
    launch_turnaround_times,
    line_of_best_fit,
    launches_in_time_interval,
    get_most_flown_stages,
    get_most_flown_spacecraft,
    StageObjects,
    build_filter,
    RegexpReplace,
)
from booster_tracker.utils import (
    concatenated_list,
    convert_seconds,
    all_zeros,
    parse_start_time,
    get_start_date,
    make_monotonic,
    MonotonicDirections,
    build_table_html,
    get_averages,
)
from rest_framework.pagination import PageNumberPagination
import pytz
import math
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
    SPACECRAFT_TYPES,
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework import status
from booster_tracker.serializers import (
    LaunchSerializer,
    LaunchOnlySerializer,
    RocketSerializer,
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
    RocketFamilyInformationSerializer,
    SpacecraftFamilyInformationSerializer,
    CalendarStatsSerializer,
    StageListSerializer,
    EDATableSerializer,
    AdditionalGraphSerializer,
    LaunchInformation2Serializer,
)
import json


class StandardPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = "page_size"


# APIViews without any additional logic
class OrbitApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """Get list of all orbits"""
        orbits = Orbit.objects.all()
        serializer = OrbitSerializer(orbits, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LaunchOnlyApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """List all the Launch items (without recoveries) for given user request"""
        launches = Launch.objects.all()
        serializer = LaunchOnlySerializer(launches, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RocketApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """List all the Rocket items for given user request"""
        rockets = Rocket.objects.all()
        serializer = RocketSerializer(rockets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RocketFamilyApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """List all the RocketFamily items for given user request"""
        rocketfamilies = RocketFamily.objects.all()
        serializer = RocketFamilySerializer(rocketfamilies, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class OperatorApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """List all the Operator items for given user request"""
        operators = Operator.objects.all()
        serializer = OperatorSerializer(operators, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BoatApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """list all of the boats for given user request"""
        boats = Boat.objects.all()
        serializer = BoatSerializer(boats, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StageAndRecoveryApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """List of all stage and recoveries"""
        stage_and_recoveries = StageAndRecovery.objects.all()
        serializer = StageAndRecoverySerializer(stage_and_recoveries, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SpacecraftFamilyApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """List of all spacecraft families"""
        spacecraft_families = SpacecraftFamily.objects.all()
        serializer = SpacecraftFamilySerializer(spacecraft_families, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# Launch Calendar Stats
class FilteredLaunchDaysApiView(APIView):
    def get(self, request) -> Response:
        """Get launch stats and launches for historical launch calendar"""
        filter = json.loads(request.query_params.get("filter"))
        filtered_launches = get_model_objects_with_filter(Launch, filter).filter(time__lte=datetime.now(pytz.utc))
        launches_on_day = launches_per_day(filtered_launches)

        num_days_with_launches = len(launches_on_day)
        percentage_days_with_launch = round(num_days_with_launches / 3.66, 2)

        max_launches = launches_on_day[0]["count"]

        days_with_most_launches = []
        for day in launches_on_day:
            if day["count"] == max_launches:
                days_with_most_launches.append(day["date"])
            else:
                break

        data = {
            "num_days_with_launches": num_days_with_launches,
            "percentage_days_with_launches": percentage_days_with_launch,
            "most_launches": max_launches,
            "days_with_most_launches": concatenated_list(days_with_most_launches),
            "launches": filtered_launches,
        }

        serializer = CalendarStatsSerializer(data)

        return Response(serializer.data)


# List API views


class LaunchApiView(ListAPIView):
    serializer_class = LaunchSerializer
    pagination_class = StandardPagination

    def get_queryset(self) -> QuerySet:
        """Return the list of launches for this view."""
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        order_by = self.request.query_params.get("order_by", "-time")

        launch_objects = get_model_objects_with_filter(Launch, filter, query)

        if "stageandrecovery" in order_by:
            # Clean up order_by string
            field_name = order_by.replace("stageandrecovery__", "").replace("-", "")
            direction = "desc" if "-" in order_by else "asc"

            # Query StageAndRecovery related launches
            launch_objects = (
                StageAndRecovery.objects.filter(launch__in=launch_objects)
                .select_related("launch")
                .order_by(
                    getattr(F(field_name), direction)(nulls_last=True),
                    F("launch__time").desc(),
                )
            )
            # Extract launches from StageAndRecovery objects
            launch_objects = [stage_and_recovery.launch for stage_and_recovery in launch_objects]
        else:
            # Clean up order_by string
            field_name = order_by.replace("-", "")
            direction = "desc" if "-" in order_by else "asc"

            # Query Launch objects
            launch_objects = launch_objects.order_by(
                getattr(F(field_name), direction)(nulls_last=True),
                F("time").desc(),
            )

        return launch_objects

    def get(self, request, *args, **kwargs) -> Response:
        """List all the Launch items for given requested user"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)

            return self.get_paginated_response(serializer.data)


class PadApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """List of all pads"""
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        filtered_pads = get_model_objects_with_filter(Pad, filter, query).order_by("-name")
        serializer = PadSerializer(filtered_pads, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class LandingZoneApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """List of all landing zones"""
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        filtered_zones = get_model_objects_with_filter(LandingZone, filter, query).order_by("-name")
        serializer = LandingZoneSerializer(filtered_zones, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class StageApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
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
            .annotate(
                extracted_value=RegexpReplace(F("name")),
                # Cast only valid floats, otherwise return NULL
                stage_number=Cast(
                    Case(
                        When(extracted_value__regex=r"^[0-9]+(\.[0-9]+)?$", then=F("extracted_value")),
                        default=None,
                        output_field=FloatField(),
                    ),
                    FloatField(),
                ),
            )
            .order_by(F("stage_number").desc(nulls_last=True))
        )

        data = {"start_filter": start_filter, "stages": filtered_stages}
        serializer = StageListSerializer(data)

        return Response(serializer.data)


class SpacecraftApiView(ListAPIView):
    def get(self, request, *args, **kwargs) -> Response:
        # Get information from URL
        filter_param = self.request.query_params.get("filter", "{}")
        filter = json.loads(filter_param)
        query = self.request.query_params.get("query", "")
        family_str = self.request.query_params.get("family", "")
        family = SpacecraftFamily.objects.get(name__icontains=family_str)

        # Prepare information
        start_filter = build_filter(model=Spacecraft, family=family, type=None)
        if family_str:
            filtered_spacecraft = get_model_objects_with_filter(Spacecraft, filter, query).filter(family=family)
        else:
            filtered_spacecraft = get_model_objects_with_filter(Spacecraft, filter, query)
        filtered_spacecraft = filtered_spacecraft.annotate(
            extracted_value=RegexpReplace(F("name")),
            # Cast only valid floats, otherwise return NULL
            spacecraft_number=Cast(
                Case(
                    When(extracted_value__regex=r"^[0-9]+(\.[0-9]+)?$", then=F("extracted_value")),
                    default=None,
                    output_field=FloatField(),
                ),
                FloatField(),
            ),
        ).order_by(F("spacecraft_number").desc(nulls_last=True), F("name").asc())

        data = {"start_filter": start_filter, "spacecraft": filtered_spacecraft}
        serializer = SpacecraftListSerializer(data)

        return Response(serializer.data)


# Information API Views


class LaunchInformationApiView(RetrieveAPIView):
    serializer_class = LaunchInformationSerializer

    def get_object(self) -> Launch:
        """Get launch by ID"""
        id = self.request.query_params.get("id", "")
        return Launch.objects.get(id=id)


class LaunchInformation2ApiView(RetrieveAPIView):
    serializer_class = LaunchInformation2Serializer

    def get_object(self) -> Launch:
        """Get launch by ID"""
        id = self.request.query_params.get("id", "")
        return Launch.objects.get(id=id)


class LandingZoneInformationApiView(RetrieveAPIView):
    def get(self, request, *args, **kwargs) -> Response:
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
    def get(self, request, *args, **kwargs) -> Response:
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
    def get(self, request, *args, **kwargs) -> Response:
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
    def get(self, request, *args, **kwargs) -> Response:
        """Get pad by ID"""
        id = self.request.query_params.get("id", "")
        pad = Pad.objects.get(id=id)
        filtered_launches = Launch.objects.filter(pad=pad).order_by("time")
        display_launches = filtered_launches.filter(time__lte=datetime.now(pytz.utc)).order_by("-time")[:25]

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
    def get(self, request) -> Response:
        """Returns response for data on home page"""
        self.now = datetime.now(pytz.utc)
        start_time = parse_start_time(self.request.query_params, self.now)
        function_type = self.request.query_params.get("functiontype", "")

        # Get launches per rocket per year:
        launches_per_rocket_per_year, years = self._get_launches_per_vehicle_per_year()

        # Get filtered launches
        filtered_launches = Launch.objects.filter(time__gte=start_time, time__lte=self.now).order_by("time")

        # Fetch basic stats
        next_launch = Launch.objects.filter(time__gt=datetime.now(pytz.utc)).last()
        last_launch = Launch.objects.filter(time__lte=datetime.now(pytz.utc)).first()
        num_missions = Launch.objects.filter(
            rocket__family__provider__name="SpaceX", time__lte=self.now, exclude_from_missions=False
        ).count()
        num_successes = Launch.objects.filter(
            rocket__family__provider__name="SpaceX",
            launch_outcome="SUCCESS",
            time__lte=self.now,
            exclude_from_missions=False,
        ).count()
        num_landings = (
            StageAndRecovery.objects.filter(Q(method="DRONE_SHIP") | Q(method="GROUND_PAD"))
            .filter(method_success="SUCCESS", launch__time__lte=self.now)
            .count()
        )
        shortest_time_between_launches = convert_seconds(
            Launch.objects.filter(rocket__family__provider__name="SpaceX", time__lte=self.now)
            .order_by("company_turnaround")
            .first()
            .company_turnaround
        )
        num_stage_reflights = self._calculate_num_stage_reflights()

        # If no filtered launches exist, return data to avoid failures
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

        # Process turnaround data and best fit calculations; use this to predict future launches
        turnaround_data = self._process_turnaround_data(filtered_launches, function_type)
        launch_predictions = self._calculate_launch_predictions(
            filtered_launches, self.now, turnaround_data["best_fit_line"]
        )

        data = {
            "turnaround_x_values": turnaround_data["x_values"],
            "turnaround_data": turnaround_data["averaged_values"],
            "best_fit_turnaround_values": turnaround_data["best_fit_turnaround_values"],
            "chunk_size": turnaround_data["chunk_size"],
            "total_launches_current_year": launch_predictions["total_launches_current_year"],
            "total_launches_next_year": launch_predictions["total_launches_next_year"],
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
    ) -> dict:
        """If no launches exist in the filter, return trivial values to avoid error"""
        return {
            "turnaround_x_values": [],
            "turnaround_data": [],
            "best_fit_turnaround_values": [],
            "chunk_size": 0,
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

    def _get_launches_per_vehicle_per_year(self) -> tuple:
        """Get the total number of launches per rocket per year; returns a tuple of following format:
        (dict(list), list) where dict has key of rocket ID and value of the list; second list is list of years from first launch to now
        """
        launches_per_rocket_per_year = {}
        current_year = self.now.year

        # Initialize a variable to track the global minimum year
        global_min_year = current_year

        # Find the global minimum year across all rockets
        global_min_year = min(
            current_year,
            Launch.objects.filter(time__lte=self.now, rocket__family__provider__name="SpaceX")
            .order_by("time")
            .first()
            .time.year,
        )

        # Get total number of launches per rocket per year; fill in years with zeros
        for rocket in Rocket.objects.filter(family__provider__name="SpaceX").order_by("-name"):
            launches_per_year = (
                Launch.objects.filter(rocket=rocket, time__lte=self.now)
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

        return (launches_per_rocket_per_year, years)

    def _calculate_num_stage_reflights(self) -> int:
        """Returns int representing the total number of times a stage has been reflown across all SpaceX families"""
        num_stage_uses = (
            StageAndRecovery.objects.filter(launch__time__lte=self.now)
            .filter(launch__rocket__family__provider__name="SpaceX")
            .count()
        )
        num_stages_used = (
            Stage.objects.filter(stageandrecovery__launch__time__lte=self.now)
            .filter(rocket__family__provider__name="SpaceX")
            .distinct()
            .count()
        )
        return num_stage_uses - num_stages_used

    def _process_turnaround_data(self, filtered_launches, function_type):
        """Given function type, calculates line of best fit and predicts number of launches in the future; returns a dict of following type:
        "turnaround_data": dict(str: float) representing time between each launche,
        "best_fit_turnaround_values": list of values calcuated from line of best fit,
        "x_values": list of values for the x axis,
        "averaged_values": shortened list with averaged values,
        "best_fit_line": equation of line of best fit,
        "chunk_size": int, representing how many launches are being averaged,
        """
        turnaround_data = launch_turnaround_times(filtered_launches=filtered_launches)
        turnaround_values = list(turnaround_data.values())

        # Limit to 40 points; to do this determine chunk size
        if not turnaround_values:
            chunk_size = 1
        else:
            chunk_size = math.ceil(len(turnaround_values) / 40)

        x_values = list(np.arange(0, len(turnaround_values), chunk_size))
        averaged_values = get_averages(turnaround_values, chunk_size, 2)
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

        best_fit_line = line_of_best_fit(
            x=all_x_values,
            y=turnaround_values,
            fit_type=function_type,
            weights=None,
            long_term_behavior_max=recent_average / 1.25,
        )

        best_fit_turnaround_values = [round(best_fit_line(x), 2) for x in x_values]

        return {
            "turnaround_data": turnaround_data,
            "best_fit_turnaround_values": best_fit_turnaround_values,
            "x_values": x_values,
            "averaged_values": averaged_values,
            "best_fit_line": best_fit_line,
            "chunk_size": chunk_size,
        }

    def _calculate_launch_predictions(self, filtered_launches, today, best_fit_line) -> dict:
        """Given a set of filtered launches and a line of best fit, returns the total number of launches predected for this year and next"""
        current_launch_number = len(filtered_launches)
        days_in_current_year = 366 if today.year % 4 == 0 else 365
        days_passed_current_year = (today - datetime(today.year, 1, 1, tzinfo=pytz.utc)).days
        remaining_days_current_year = days_in_current_year - days_passed_current_year

        launches_this_year = Launch.objects.filter(
            time__gte=(datetime(today.year, 1, 1, tzinfo=pytz.utc)),
            time__lte=self.now,
            rocket__family__provider__name="SpaceX",
        ).count()

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

        return {
            "total_launches_current_year": remaining_launches_current_year + launches_this_year,
            "total_launches_next_year": next_year_launches - (current_launch_number + remaining_launches_current_year),
        }


class RocketFamilyInformationApiView(APIView):
    def get(self, request) -> Response:
        """Generates response for family information"""
        self.now = datetime.now(pytz.utc)
        family = RocketFamily.objects.get(name__icontains=request.query_params.get("family", "None"))
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
        serializer = RocketFamilyInformationSerializer(data)

        # Return the serialized data as a response
        return Response(serializer.data)

    def _get_launch_years(self, family) -> tuple:
        """Returns current year and start year for stat graph"""
        first_launch_year = Launch.objects.filter(rocket__family=family).order_by("time").first().time
        current_year = self.now.year
        start_year = parse_start_time(self.request.query_params, first_launch_year).year

        return (start_year, current_year)

    def _get_flight_data(self, family, start_year, current_year) -> tuple:
        """Get the max number of flights of booster, fairing, and stage two, along with booster and stage two average"""
        # Create a list of years in the range
        x_axis = list(range(start_year, current_year + 1))

        # Create a single queryset for all necessary data, grouped by year
        flight_data = (
            StageAndRecovery.objects.filter(
                stage__rocket__family=family,
                launch__time__year__gte=start_year,
                launch__time__lte=self.now,
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
                launch__time__lte=self.now,
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
        max_booster_flights = make_monotonic(list(max_booster_flights.values()), MonotonicDirections.INCREASING)
        avg_booster_flights = avg_booster_flights.values()
        max_stage_two_flights = make_monotonic(list(max_stage_two_flights.values()), MonotonicDirections.INCREASING)
        avg_stage_two_flights = avg_stage_two_flights.values()
        max_fairing_flights = make_monotonic(list(max_fairing_flights.values()), MonotonicDirections.INCREASING)

        return (
            max_booster_flights,
            avg_booster_flights,
            max_fairing_flights,
            max_stage_two_flights,
            avg_stage_two_flights,
            x_axis,
        )

    def _get_family_stats(self, family) -> dict:
        """Returns the number of missions, landings, and reuses of the rocket family"""
        num_launches = Launch.objects.filter(
            rocket__family__name=family, time__lte=self.now, launch_precluded=False
        ).count()
        num_landings = StageAndRecovery.objects.filter(
            launch__rocket__family__name=family,
            method__in=["DRONE_SHIP", "GROUND_PAD", "CATCH"],
            method_success="SUCCESS",
            launch__time__lte=self.now,
        ).count()

        family_stats = {
            "Launches": str(num_launches),
            "Landings": str(num_landings),
            "Reuses": str(
                StageAndRecovery.objects.filter(
                    launch__rocket__family__name=family, num_flights__gt=1, launch__time__lte=self.now
                ).count()
            ),
        }
        return family_stats

    def _get_family_children_stats(self, family) -> dict:
        """Returns dict with stats for each rocket in the rocket family"""
        family_children_stats = {}

        for rocket in Rocket.objects.filter(family__name=family).order_by("id"):
            booster_reflights = StageAndRecovery.objects.filter(
                launch__rocket__name=rocket.name,
                num_flights__gt=1,
                stage__type=StageObjects.BOOSTER,
                launch__time__lte=self.now,
            ).count()
            stage_two_reflights = StageAndRecovery.objects.filter(
                launch__rocket__name=rocket.name,
                num_flights__gt=1,
                stage__type=StageObjects.SECOND_STAGE,
                launch__time__lte=self.now,
            ).count()
            launches = Launch.objects.filter(rocket=rocket, time__lte=self.now, launch_precluded=False).count()
            successes = Launch.objects.filter(rocket=rocket, launch_outcome="SUCCESS", time__lte=self.now).count()
            flight_proven_launches = (
                Launch.objects.filter(rocket=rocket, time__lte=self.now, stageandrecovery__num_flights__gt=1)
                .distinct()
                .count()
            )

            family_children_stats[rocket.name] = {
                "Launches": str(launches),
                "Successes": str(successes),
                "Booster Reflights": str(booster_reflights),
                "2nd Stage Reflights": str(stage_two_reflights),
                "Flight Proven Launches": str(flight_proven_launches),
            }

        return family_children_stats

    def _get_stage_stats(self, family) -> tuple:
        """Returns tuple with stage with fastest turnaround and most launches"""
        booster_most_flight_stats = get_most_flown_stages(
            family=family, stage_type=StageObjects.BOOSTER, before_date=self.now
        )
        stage_two_most_flight_stats = get_most_flown_stages(
            family=family, stage_type=StageObjects.SECOND_STAGE, before_date=self.now
        )

        quickest_booster_stage_and_recovery = (
            StageAndRecovery.objects.filter(
                stage__rocket__family=family, stage__type="BOOSTER", launch__time__lte=self.now
            )
            .exclude(stage_turnaround__isnull=True)
            .order_by("stage_turnaround")
            .first()
        )
        quickest_stage_two_stage_and_recovery = (
            StageAndRecovery.objects.filter(
                stage__rocket__family=family, stage__type="SECOND_STAGE", launch__time__lte=self.now
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
            booster_most_flight_stats["stages"] or [],
            stage_two_most_flight_stats["stages"] or [],
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
    ) -> dict:
        """Removes any trivial stats from rocket family stats"""
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


class SpacecraftFamilyInformationApiView(APIView):
    def get(self, request) -> Response:
        """Generates response for family information"""
        self.now = datetime.now(pytz.utc)
        try:
            family = SpacecraftFamily.objects.get(name__icontains=request.query_params.get("family", ""))
        except ObjectDoesNotExist:
            return HttpResponseNotFound(content="Spacecraft family not found")

        if launch := Launch.objects.filter(spacecraftonlaunch__spacecraft__family=family).order_by("time").first():
            first_launch_time = launch.time
            current_year = self.now.year
            start_year = parse_start_time(self.request.query_params, first_launch_time).year
        else:
            first_launch_time = None
            current_year = None
            start_year = None

        (
            max_spacecraft_flights,
            avg_spacecraft_flights,
            x_axis,
        ) = self._get_flight_data(family, start_year, current_year)
        family_stats = self._get_family_stats(family)
        family_children_stats = self._get_family_children_stats(family)
        (
            spacecraft_with_most_flights,
            spacecraft_with_quickest_turnaround,
            spacecraft_turnaround_time,
        ) = self._get_spacecraft_stats(family)
        series_data = self._get_series_data(max_spacecraft_flights, avg_spacecraft_flights)

        # Compile all collected data into a single dictionary
        data = {
            "launch_years": x_axis,
            "series_data": series_data,
            "stats": family_stats,
            "children_stats": family_children_stats,
            "spacecraft_with_most_flights": spacecraft_with_most_flights or [],
            "spacecraft_with_quickest_turnaround": spacecraft_with_quickest_turnaround,
            "spacecraft_turnaround_time": spacecraft_turnaround_time,
            "start_date": first_launch_time,
        }

        # Serialize the data
        serializer = SpacecraftFamilyInformationSerializer(data)

        # Return the serialized data as a response
        return Response(serializer.data)

    def _get_flight_data(self, family, start_year, current_year) -> tuple:
        """Get the max and avg num of spacecraft flights"""
        # Create a list of years in the range
        if not start_year:
            return [], [], []
        x_axis = list(range(start_year, current_year + 1))

        # Create a single queryset for all necessary data, grouped by year
        flight_data = (
            SpacecraftOnLaunch.objects.filter(
                spacecraft__family=family,
                launch__time__year__gte=start_year,
                launch__time__lte=self.now,
            )
            .annotate(year=ExtractYear("launch__time"))
            .values("year")
            .annotate(
                max_flights=Max("num_flights"),
                avg_flights=Avg("num_flights"),
            )
            .order_by("year")
        )

        # Initialize dictionaries to hold the max and avg flights for each stage type by year
        max_spacecraft_flights = {year: 0 for year in x_axis}
        avg_spacecraft_flights = {year: 0 for year in x_axis}

        # Populate spacecraft data from query set
        for data in flight_data:
            year = data["year"]
            max_spacecraft_flights[year] = data["max_flights"]
            avg_spacecraft_flights[year] = round(data["avg_flights"], 2)

        # Convert dictionaries to lists for return
        max_spacecraft_flights = make_monotonic(list(max_spacecraft_flights.values()), MonotonicDirections.INCREASING)
        avg_spacecraft_flights = avg_spacecraft_flights.values()

        return (
            max_spacecraft_flights,
            avg_spacecraft_flights,
            x_axis,
        )

    def _get_family_stats(self, family) -> dict:
        """Returns time on orbit, number of launches, and number of reuses"""
        num_launches = Launch.objects.filter(
            spacecraftonlaunch__spacecraft__family=family, time__lte=self.now, launch_precluded=False
        ).count()
        num_reuses = SpacecraftOnLaunch.objects.filter(
            spacecraft__family=family, num_flights__gt=1, launch__time__lte=self.now
        ).count()

        time_on_orbit = (
            SpacecraftOnLaunch.objects.filter(spacecraft__family=family)
            .annotate(
                orbit_duration=Case(
                    When(splashdown_time__isnull=False, then=F("splashdown_time") - F("launch__time")),
                    When(
                        splashdown_time__isnull=True,
                        then=ExpressionWrapper(self.now - F("launch__time"), output_field=DurationField()),
                    ),
                )
            )
            .aggregate(total_time_on_orbit=Sum("orbit_duration"))["total_time_on_orbit"]
            .total_seconds()
        )

        family_stats = {
            "Launches": str(num_launches),
            "Reuses": str(num_reuses),
            "Time On Orbit:": f"{time_on_orbit / 86400 :,.2f} days",
        }
        return family_stats

    def _get_family_children_stats(self, family) -> dict:
        """Returns dict with stats for each rocket in the rocket family"""
        family_children_stats = {}

        for spacecraft_type in SPACECRAFT_TYPES:
            spacecraft_reflights = SpacecraftOnLaunch.objects.filter(
                spacecraft__family=family,
                spacecraft__type=spacecraft_type[0],
                num_flights__gt=1,
                launch__time__lte=self.now,
            ).count()

            launches = Launch.objects.filter(
                spacecraftonlaunch__spacecraft__family=family,
                spacecraftonlaunch__spacecraft__type=spacecraft_type[0],
                time__lte=self.now,
                launch_precluded=False,
            ).count()

            family_children_stats[spacecraft_type[1].title()] = {
                "Launches": str(launches),
                "Reuses": str(spacecraft_reflights),
            }

        return family_children_stats

    def _get_spacecraft_stats(self, family) -> tuple:
        """Returns tuple with stage with fastest turnaround and most launches"""
        spacecraft_with_most_launches = get_most_flown_spacecraft(family=family, before_date=self.now)

        quickest_spacecraft_on_launch = (
            SpacecraftOnLaunch.objects.filter(spacecraft__family=family, launch__time__lte=self.now)
            .exclude(spacecraft_turnaround__isnull=True)
            .order_by("spacecraft_turnaround")
            .first()
        )

        if quickest_spacecraft_on_launch:
            spacecraft_with_quickest_turnaround = quickest_spacecraft_on_launch.spacecraft
            spacecraft_turnaround_time = convert_seconds(quickest_spacecraft_on_launch.spacecraft_turnaround)
        else:
            spacecraft_with_quickest_turnaround = None
            spacecraft_turnaround_time = None

        return (
            spacecraft_with_most_launches["spacecraft"],
            spacecraft_with_quickest_turnaround,
            spacecraft_turnaround_time,
        )

    def _get_series_data(self, max_spacecraft_flights, avg_spacecraft_flights) -> dict:
        """Removes any trivial stats from rocket family stats"""
        series_data = {
            "Max Spacecraft": max_spacecraft_flights,
            "Avg Spacecraft": avg_spacecraft_flights,
        }

        # Filter out entries where all values are zero
        filtered_series_data = {k: v for k, v in series_data.items() if not all_zeros(v)}

        return filtered_series_data


class EDAApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """Creates EDA table for launch"""
        name = self.request.query_params.get("name", "")
        try:
            launch = Launch.objects.get(name=name)
            launch_table = build_table_html(launch.create_launch_table())
        except launch.DoesNotExist:
            return HttpResponseNotFound("Launch not found")

        # Compile all collected data into a single dictionary
        data = {
            "launch_table": launch_table,
        }

        # Serialize the data
        serializer = EDATableSerializer(data)

        # Return the serialized data as a response
        return Response(serializer.data)


class AdditionalGraphsApiView(APIView):
    def get(self, request, *args, **kwargs) -> Response:
        """Creates additional graphs"""
        self.now = datetime.now(pytz.utc)
        mass_per_year = self._get_mass_to_orbit_per_year(provider=Operator.objects.get(name="SpaceX"))

        data = {"mass_per_year": mass_per_year}

        serializer = AdditionalGraphSerializer(data)
        return Response(serializer.data)

    def _get_mass_to_orbit_per_year(self, provider) -> dict:
        """Returns total mass launched to orbit per year"""
        mass_per_year = (
            Launch.objects.filter(
                rocket__family__provider=provider, time__lte=self.now, launch_outcome__in=["SUCCESS", "PARTIAL_FAILURE"]
            )
            .exclude(orbit__name="Sub-orbital")
            .annotate(year=ExtractYear("time"))
            .values("year")
            .annotate(sum=Coalesce(Sum("mass") / 1000, Value(0)))
            .order_by("year")
        )

        global_min_year = self.now.year

        if mass_per_year.exists():
            min_year = min(entry["year"] for entry in mass_per_year)
            global_min_year = min(global_min_year, min_year)

        # Convert the queryset to a dictionary
        formatted_dict = {entry["year"]: entry["sum"] for entry in mass_per_year}

        # Fill in missing years with zeros from global_min_year to current_year
        for year in range(global_min_year, self.now.year + 1):
            if year not in formatted_dict:
                formatted_dict[year] = 0

        # Sort the dictionary by year
        mass_per_year = dict(sorted(formatted_dict.items()))

        return mass_per_year
