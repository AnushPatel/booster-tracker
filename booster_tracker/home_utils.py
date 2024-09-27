from django.db.models import Q, Count, Max, Avg
from django.db import models
from django.apps import apps
from booster_tracker.models import (
    Stage,
    StageAndRecovery,
    Pad,
    PadUsed,
    Boat,
    Rocket,
    LandingZone,
    Launch,
    RocketFamily,
    Spacecraft,
)
from booster_tracker.utils import (
    all_values_true,
    version_format,
    combine_dicts,
)
from datetime import datetime
from django.templatetags.static import static
import pytz
from enum import StrEnum
from collections import defaultdict
import numpy as np
from scipy.optimize import curve_fit
from scipy.integrate import quad


class StageObjects(StrEnum):
    BOOSTER = "BOOSTER"
    SECOND_STAGE = "SECOND_STAGE"


def get_most_flown_stages(family: RocketFamily, stage_type: StageObjects, before_date: datetime):
    """Returns the stage(s) with the highest number of flights, and how many flights that is"""
    stage_and_launch_count = StageAndRecovery.objects.filter(
        launch__time__lte=before_date, stage__type=stage_type, stage__rocket__family=family
    ).order_by("-num_flights", "stage__name")

    if not stage_and_launch_count:
        return {
            "stages": None,
            "num_launches": 0,
        }
    max_launch_count = stage_and_launch_count[0].num_flights

    most_flown_stages = list(item.stage for item in stage_and_launch_count.filter(num_flights=max_launch_count))

    return {
        "stages": most_flown_stages,
        "num_launches": max_launch_count if max_launch_count else 0,
    }


def get_next_and_last_launches():
    """Gets the next launch and last launch"""
    next_launch = Launch.objects.filter(time__gt=datetime.now(pytz.utc)).last()
    last_launch = Launch.objects.filter(time__lte=datetime.now(pytz.utc)).first()
    return next_launch, last_launch


# This section deals with functions that are used by the API


def get_true_filter_values(filter, filter_item):
    true_values = {}
    for value in filter[filter_item].values():
        if isinstance(value, dict):
            # If the value is a dict, need to go one layer further in to get the data. Ex: {"rocket__family": {"rocket": {"1": True, "2": True}}} should look at "rockets" since this contains all information about parent filter
            for child_filter_item in filter[filter_item].keys():
                true_values = combine_dicts(true_values, get_true_filter_values(filter[filter_item], child_filter_item))
        else:
            # If there is not a dict, then find the values which are true
            true_values_for_filter_name = []
            for key, value in filter[filter_item].items():
                if value:
                    # If the string is an int, convert it for query purposes. Strings vs int determined by database storage type
                    formatted_key = lambda key: (int(key) if key.isnumeric() else version_format(key.upper()))
                    true_values_for_filter_name.append(formatted_key(key))
            true_values[filter_item] = true_values_for_filter_name

    return true_values


def get_model_objects_with_filter(model: models.Model, filter: dict, search_query: str = ""):
    """Takes in a filter and returns all launch objects that obey one of those filters"""

    if (not filter and not search_query) or (all_values_true(filter) and not search_query):
        return model.objects.all()

    true_values = {}

    for filter_item in filter.keys():
        # Cycles through filter to get all values that are true into a list; ex {"rocket": {"1": True, "2": False, "3": True}} => {"rocket": [1, 2, 3]}
        true_values_from_item = get_true_filter_values(filter, filter_item)
        true_values = true_values | true_values_from_item

    non_ids = [
        "launch_outcome",
        "hide__stageandrecovery__method",
        "stageandrecovery__method_success",
        "status",
        "version",
        "type",
    ]
    objects_or = [["hide__stageandrecovery__method", "hide__stageandrecovery__landing_zone"]]

    q_objects = Q()

    for key, value in true_values.items():
        if key not in sum(objects_or, []):  # Check if key is not in any list in objects_or
            if key in non_ids:
                q_objects &= Q(**{f"{key.replace('hide__', '')}__in": value})
            else:
                q_objects &= Q(**{f"{key.replace('hide__', '')}__id__in": value})

    or_queries = []

    for or_list in objects_or:
        if any(field in true_values for field in or_list):
            or_query = Q()
            for field in or_list:
                if field in non_ids:
                    or_query |= Q(**{f"{field.replace('hide__', '')}__in": true_values.get(field, [])})
                else:
                    or_query |= Q(**{f"{field.replace('hide__', '')}__id__in": true_values.get(field, [])})

            or_queries.append(or_query)

    if or_queries:
        for query in or_queries:
            q_objects &= query

    filtered_objects = model.objects.filter(q_objects).filter(name__icontains=search_query).distinct().all()

    return filtered_objects


def launches_per_day(launches: list[Launch]):
    """Takes in a list of launches and gives the number of launches on each day (excluding year)"""
    launches_per_day = defaultdict(int)
    for launch in launches:
        date = f"{launch.time.strftime('%B %d')}"
        launches_per_day[date] += 1

    launches_per_day = sorted(launches_per_day.items(), key=lambda x: x[1], reverse=True)

    return launches_per_day


def launch_turnaround_times(filtered_launches: list[Launch]):
    turnaround_times = {}
    for launch in filtered_launches:
        if time := (launch.company_turnaround):
            turnaround_times[launch.name] = round(time / 86400, 2)

    return turnaround_times


def line_of_best_fit(x: list, y: list, fit_type="exponential", weights=None, long_term_behavior_max=2.5):
    # Linear fit
    if fit_type == "linear":
        coeffs = np.polyfit(x, y, 1)
        fit_func = np.poly1d(coeffs)

    # Quadratic fit
    elif fit_type == "quadratic":
        coeffs = np.polyfit(x, y, 2)
        fit_func = np.poly1d(coeffs)

    # Cubic fit
    elif fit_type == "cubic":
        coeffs = np.polyfit(x, y, 3)
        fit_func = np.poly1d(coeffs)

    # Exponential fit
    elif fit_type == "exponential":

        def exp_func(x, a, b, c):
            return a * np.exp(b * x) + c

        # Better initial guess for exponential decay
        initial_guess = (y[0] - y[-1], -0.5, 0.5)

        bounds = ([-np.inf, -np.inf, 0], [np.inf, np.inf, long_term_behavior_max])

        if weights is None:
            weights = np.ones_like(x)
            # weights[-(int(len(x) * 0.40)) :] = 10

        coeffs, _ = curve_fit(exp_func, x, y, p0=initial_guess, maxfev=10000, sigma=weights, bounds=bounds)
        fit_func = lambda x: exp_func(x, *coeffs)

    return fit_func


# Define a function to find the cumulative days for a given range of launch numbers
def time_between_launches(line_of_best_fit, start_launch: Launch, end_launch: Launch, min_value: float):
    """Using a line of best fit (launches (x) vs time/launch (y)), calculates the time between two launches; if the integral is less than or equal to 0, it returns min value"""
    integral, _ = quad(line_of_best_fit, start_launch, end_launch)
    if integral <= 0:
        return min_value
    return integral


def launches_in_time_interval(line_of_best_fit, start_launch_num: int, remaining_days: int, min_value: float):
    """with a line of best fit, figures out the number of launches left in the remaining time interval. start_launch_num x-axis int of integration starting point"""
    end_launch_num = start_launch_num
    days_integrated = 0
    while days_integrated < remaining_days:
        days_integrated += time_between_launches(
            line_of_best_fit=line_of_best_fit,
            start_launch=end_launch_num,
            end_launch=end_launch_num + 1,
            min_value=min_value,
        )
        end_launch_num += 1
    return end_launch_num


def build_filter(model: models.Model, family: models.Model, type: StageObjects):
    rockets = set()
    versions = set()
    types = set()
    statuses = set()

    q_objects = Q()

    if model == Stage:
        q_objects &= Q(**{f"rocket__family": family})
        q_objects &= Q(**{f"type": type})
    elif model == Spacecraft:
        q_objects &= Q(**{f"family": family})

    for child in model.objects.filter(q_objects):
        if hasattr(child, "version"):
            versions.add(child.version)
        if hasattr(child, "status"):
            statuses.add(child.status)
        if hasattr(child, "rocket"):
            rockets.add(child.rocket.id)
        if not model == Stage and hasattr(child, "type"):
            types.add(child.type)

    filter = {}

    if rockets:
        filter_item = {}
        for rocket in sorted(list(rockets), reverse=True):
            filter_item[f"{rocket}"] = True
        filter["rocket"] = filter_item

    if versions:
        filter_item = {}
        for version in sorted(list(versions), reverse=True):
            filter_item[f"{version}"] = True
        filter["version"] = filter_item

    if statuses:
        filter_item = {}
        for status in sorted(list(statuses)):
            filter_item[f"{status}"] = True
        filter["status"] = filter_item

    if types:
        filter_item = {}
        for type in sorted(list(types)):
            filter_item[f"{type}"] = True
        filter["type"] = filter_item

    return filter
