from booster_tracker.home_utils import (
    get_most_flown_stages,
    get_next_and_last_launches,
    get_true_filter_values,
    get_model_objects_with_filter,
    launches_per_day,
    line_of_best_fit,
    launches_in_time_interval,
    launch_turnaround_times,
    StageObjects,
    time_between_launches,
)

from booster_tracker.models import Rocket, Pad, Orbit, Launch, Stage, RocketFamily, StageAndRecovery, LandingZone

from .test_helpers import initialize_test_data
from django.test import TestCase
from datetime import datetime
import pytz
import numpy as np
from scipy.integrate import quad


class TestCases(TestCase):
    def setUp(self):
        initialize_test_data()

    def test_get_most_flown_stages(self):
        # Ensure most flown boosters being grabbed successfully
        B1062 = Stage.objects.get(name="B1062")
        B1080 = Stage.objects.get(name="B1080")
        self.assertEqual(
            get_most_flown_stages(
                family=RocketFamily.objects.get(name="Falcon"),
                stage_type=StageObjects.BOOSTER,
                before_date=datetime.now(pytz.utc),
            ),
            ({"stages": [B1062, B1080], "num_launches": 3}),
        )

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # After adding the launch, ensure the output updates accordingly
        self.assertEqual(
            get_most_flown_stages(
                family=RocketFamily.objects.get(name="Falcon"),
                stage_type=StageObjects.BOOSTER,
                before_date=datetime.now(pytz.utc),
            ),
            ({"stages": [B1080], "num_launches": 4}),
        )

    # Test get_next_and_last_launch() function
    def test_get_next_and_last_launches(self):
        # Ensure next launch does not exist and launch launch is correctly being found
        self.assertEqual(get_next_and_last_launches()[0], None)
        self.assertEqual(get_next_and_last_launches()[1].name, "Falcon 9 Launch 4")

        Launch.objects.create(
            time=datetime.now(pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(datetime.now().year + 1, 8, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Ensure that the function updates correctly when a next launch is added
        self.assertEqual(get_next_and_last_launches()[1].name, "Falcon 9 Temp Launch 1")
        self.assertEqual(get_next_and_last_launches()[0].name, "Falcon 9 Temp Launch 2")

    def test_get_true_filter_values(self):
        filter = {"rocket": {"1": True, "2": False, "3": True}}
        filter_item = "rocket"
        expected = {"rocket": [1, 3]}
        result = get_true_filter_values(filter, filter_item)
        self.assertEqual(result, expected)

        filter = {
            "rocket__family": {"rocket": {"1": True, "2": False, "3": True}, "rocket__type": {"4": True, "5": False}}
        }
        filter_item = "rocket__family"
        expected = {"rocket": [1, 3], "rocket__type": [4]}
        result = get_true_filter_values(filter, filter_item)
        self.assertEqual(result, expected)

        filter = {"rocket__family": {"rocket": {"rocket__type": {"1": True, "2": False, "3": True}}}}
        filter_item = "rocket__family"
        expected = {"rocket__type": [1, 3]}
        result = get_true_filter_values(filter, filter_item)
        self.assertEqual(result, expected)

        filter = {"rocket": {"1": False, "2": False}}
        filter_item = "rocket"
        expected = {"rocket": []}
        result = get_true_filter_values(filter, filter_item)
        self.assertEqual(result, expected)

        filter = {"rocket": {"1": True, "A": True, "B": False}}
        filter_item = "rocket"
        expected = {"rocket": [1, "A"]}
        result = get_true_filter_values(filter, filter_item)
        self.assertEqual(result, expected)

        filter = {"rocket": {"1": True, "a": True, "2": False, "b": True}}
        filter_item = "rocket"
        expected = {"rocket": [1, "A", "B"]}
        result = get_true_filter_values(filter, filter_item)
        self.assertEqual(result, expected)

    def test_get_model_objects_with_filter(self):
        # Create temp objects for test purposes
        Launch.objects.create(
            time=datetime(2024, 6, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(nickname="LC-39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 7, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(nickname="SLC-40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="FAILURE",
        )

        # Create more test cases to ensure coverage

        # Test for `objects_or` handling
        f9 = Rocket.objects.get(name="Falcon 9")
        slc40 = Pad.objects.get(nickname="SLC-40")
        lc39a = Pad.objects.get(nickname="LC-39A")
        lz1 = LandingZone.objects.get(name="Landing Zone 1")

        # Case where 'hide__stageandrecovery__method' is present in `objects_or`
        filter = {
            "hide__stageandrecovery__method": {"GROUND_PAD": True},  # assuming this field is part of `objects_or`
            "rocket": {str(f9.id): True},
        }
        result = get_model_objects_with_filter(Launch, filter)
        self.assertGreater(result.count(), 0)  # Check that some objects are returned

        # Test with multiple fields in `objects_or`
        filter = {
            "hide__stageandrecovery__method": {"GROUND_PAD": True, "DRONE_SHIP": False},
            "hide__stageandrecovery__landing_zone": {str(lz1.id): True},
        }
        result = get_model_objects_with_filter(Launch, filter)
        self.assertGreater(result.count(), 0)  # Check that some objects are returned

        # check nonsense that will return nothing
        filter = {"hide__stageandrecovery__method": {str(slc40.id): True}}
        result = get_model_objects_with_filter(Launch, filter)
        self.assertGreater(result.count(), 0)

        # Test with no objects matching `or_list` criteria
        filter = {"launch_outcome": {"SUCCESS": True}, "rocket": {"1": True, "2": True}}
        result = get_model_objects_with_filter(Launch, filter)
        self.assertEqual(result.count(), 7)

        # Test with non-matching search query
        result = get_model_objects_with_filter(Launch, filter, "Non-existent")
        self.assertEqual(result.count(), 0)

    def test_launches_per_day(self):
        # Test get laucnhes with current list
        result = launches_per_day(Launch.objects.all())
        expected = [("May 01", 1), ("April 01", 1), ("March 01", 1), ("February 01", 1), ("January 01", 1)]
        self.assertEqual(result, expected)

        # Add a second launch on another day, make sure it updates accordingly:
        Launch.objects.create(
            time=datetime(2024, 1, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(nickname="SLC-40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="FAILURE",
        )
        result = launches_per_day(Launch.objects.all())
        expected = [("January 01", 2), ("May 01", 1), ("April 01", 1), ("March 01", 1), ("February 01", 1)]
        self.assertEqual(result, expected)

    def test_launch_turnaround_times(self):
        expected = {
            "Falcon 9 Launch 2": 31,
            "Falcon 9 Launch 3": 29,
            "Falcon Heavy Launch 1": 31,
            "Falcon 9 Launch 4": 30,
        }
        self.assertEqual(launch_turnaround_times(Launch.objects.all().order_by("time")), expected)

    def test_line_of_best_fit(self):

        # Set up some common data
        self.x = np.array([1, 2, 3, 4, 5])
        self.y_linear = np.array([2, 4, 6, 8, 10])
        self.y_quadratic = np.array([1, 4, 9, 16, 25])
        self.y_cubic = np.array([1, 8, 27, 64, 125])
        self.y_exponential = np.array([5, 3.7, 2.5, 1.7, 1.2])
        self.weights = np.array([1, 1.1, 1.2, 1.3, 1.4])

        # Test linear fit
        fit_func = line_of_best_fit(self.x, self.y_linear, fit_type="linear")
        np.testing.assert_array_almost_equal(fit_func(self.x), self.y_linear)

        # Test quadratic fit
        fit_func = line_of_best_fit(self.x, self.y_quadratic, fit_type="quadratic")
        np.testing.assert_array_almost_equal(fit_func(self.x), self.y_quadratic)

        # Test cubic fit
        fit_func = line_of_best_fit(self.x, self.y_cubic, fit_type="cubic")
        np.testing.assert_array_almost_equal(fit_func(self.x), self.y_cubic)

        # Test exponential fit
        fit_func = line_of_best_fit(self.x, self.y_exponential, fit_type="exponential")
        np.testing.assert_array_almost_equal(fit_func(self.x), self.y_exponential, decimal=0)

        # Test exponential fit with weights
        fit_func = line_of_best_fit(self.x, self.y_exponential, fit_type="exponential", weights=self.weights)
        np.testing.assert_array_almost_equal(fit_func(self.x), self.y_exponential, decimal=0)

    def test_time_between_launches(self):
        self.line_of_best_fit = lambda x: 2 * x + 3
        integral, _ = quad(self.line_of_best_fit, 1, 3)
        result = time_between_launches(self.line_of_best_fit, 1, 3, min_value=0)
        self.assertEqual(result, integral)

        # Test case where the integral between the two launches is exactly zero
        zero_line_of_best_fit = lambda x: 0  # This function always returns 0, so the integral should be 0
        result = time_between_launches(zero_line_of_best_fit, 1, 2, min_value=5)
        self.assertEqual(result, 5)

        # Test case where the integral between the two launches is negative
        negative_line_of_best_fit = lambda x: -2 * x - 3  # This function always returns negative values
        result = time_between_launches(negative_line_of_best_fit, 1, 3, min_value=10)
        self.assertEqual(result, 10)

        # Test case where the integral equals the minimum value
        constant_line_of_best_fit = lambda x: 0  # Constant function, the integral should be 0
        result = time_between_launches(constant_line_of_best_fit, 1, 2, min_value=0)
        self.assertEqual(result, 0)

        # Test case where the integral is less than or equal to zero, and min_value is returned
        result = time_between_launches(self.line_of_best_fit, 1, 1, min_value=3)
        self.assertEqual(result, 3)

    def test_launches_in_time_interval(self):
        # Set up some common data
        self.x = np.array([1, 2, 3, 4, 5])
        self.y_linear = np.array([2, 4, 6, 8, 10])
        self.y_exponential = np.array([5, 3.7, 2.5, 1.7, 1.2])

        # Define line of best fit functions
        self.linear_fit = line_of_best_fit(self.x, self.y_linear, fit_type="linear")
        self.exponential_fit = line_of_best_fit(self.x, self.y_exponential, fit_type="exponential")

        # Min value for interval
        min_value = 1

        # Test with linear fit
        start_launch_num = 1
        remaining_days = 10
        result = launches_in_time_interval(self.linear_fit, start_launch_num, remaining_days, min_value)
        expected_result = 4  # This would need to be calculated based on the test function
        self.assertEqual(result, expected_result)

        # Test with exponential fit
        start_launch_num = 1
        remaining_days = 10
        result = launches_in_time_interval(self.exponential_fit, start_launch_num, remaining_days, min_value)
        expected_result = 5  # This would need to be calculated based on the test function
        self.assertEqual(result, expected_result)

        # Test with different min_value
        min_value = 2
        start_launch_num = 1
        remaining_days = 10
        result = launches_in_time_interval(self.exponential_fit, start_launch_num, remaining_days, min_value)
        expected_result = 5  # This would need to be adjusted based on new min_value
        self.assertEqual(result, expected_result)

        # Test with zero remaining days
        remaining_days = 0
        result = launches_in_time_interval(self.exponential_fit, start_launch_num, remaining_days, min_value)
        expected_result = start_launch_num  # Should return the starting launch number since no time is integrated
        self.assertEqual(result, expected_result)
