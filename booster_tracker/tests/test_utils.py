from booster_tracker.utils import (
    format_time,
    convert_seconds,
    make_ordinal,
    concatenated_list,
    all_values_true,
    version_format,
    get_averages,
    make_monotonic,
    MonotonicDirections,
    all_zeros,
    combine_dicts,
    turnaround_time,
    parse_start_time,
)

from booster_tracker.models import (
    Rocket,
    Pad,
    Orbit,
    Launch,
)

from .test_helpers import initialize_test_data
from django.test import TestCase
from datetime import datetime
import pytz


class TestCases(TestCase):
    def setUp(self):
        initialize_test_data()

    def test_format_time(self):
        self.assertEqual(
            format_time(datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc)),
            "January 01, 2024 - 00:00 UTC",
        )
        self.assertEqual(
            format_time(datetime(2024, 3, 14, 14, 32, tzinfo=pytz.utc)),
            "March 14, 2024 - 14:32 UTC",
        )

    def test_convert_seconds(self):
        self.assertEqual(convert_seconds(90061), "1 day, 1 hour, 1 minute, and 1 second")
        self.assertEqual(convert_seconds(195330), "2 days, 6 hours, 15 minutes, and 30 seconds")
        self.assertEqual(convert_seconds(345650), "4 days and 50 seconds")
        self.assertEqual(convert_seconds(95400), "1 day, 2 hours, and 30 minutes")
        self.assertEqual(convert_seconds(36610), "10 hours, 10 minutes, and 10 seconds")
        self.assertEqual(convert_seconds(355), "5 minutes and 55 seconds")
        self.assertEqual(convert_seconds(0), "0 seconds")

    def test_make_ordinal(self):
        self.assertEqual(make_ordinal(None), "None")
        self.assertEqual(make_ordinal(13), "13th")
        self.assertEqual(make_ordinal(0), "0th")
        self.assertEqual(make_ordinal(1), "1st")
        self.assertEqual(make_ordinal(2), "2nd")
        self.assertEqual(make_ordinal(3), "3rd")
        self.assertEqual(make_ordinal(4), "4th")
        self.assertEqual(make_ordinal(31), "31st")

    def test_concatinated_list(self):
        self.assertEqual(concatenated_list(["Bob", "Doug", "GO Beyond"]), "Bob, Doug, and GO Beyond")
        self.assertEqual(concatenated_list(["Bob", "Doug"]), "Bob and Doug")
        self.assertEqual(concatenated_list(["Bob"]), "Bob")
        self.assertEqual(concatenated_list([]), "N/A")

    def test_turnaround_time(self):
        self.assertIsNone(turnaround_time([]))
        self.assertEqual(turnaround_time(Launch.objects.all().order_by("time")), 2592000)

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Ensure function responds according to launch addition
        self.assertEqual(turnaround_time(Launch.objects.all().order_by("time")), 86400)

    def test_all_values_true(self):
        test1 = {1: True, 2: {3: True, 4: {5: {6: True}, 7: True}}}
        test2 = {1: True}
        test3 = {1: False}
        test4 = {1: True, 2: {3: False}}

        self.assertEqual(all_values_true(test1), True)
        self.assertEqual(all_values_true(test2), True)
        self.assertEqual(all_values_true(test3), False)
        self.assertEqual(all_values_true(test4), False)
        self.assertEqual(all_values_true(None), False)

    def test_version_format(self):
        str1 = "V1.0"
        str2 = "v1.0"
        str3 = "Version"

        self.assertEqual(version_format(str1), "v1.0")
        self.assertEqual(version_format(str2), "v1.0")
        self.assertEqual(version_format(str3), "Version")

    def test_get_averages(self):
        self.assertEqual(get_averages([1, 2, 3, 4, 5, 6], 2), [1.5, 3.5, 5.5])
        self.assertEqual(get_averages([1, 2, 3, 4, 5], 10), [3.0])
        self.assertEqual(get_averages([1, 2, 3, 4, 5], 5), [3.0])
        self.assertEqual(get_averages([], 3), [])
        self.assertEqual(get_averages([1, 2, 3, 4, 5], 1), [1, 2, 3, 4, 5])
        self.assertEqual(get_averages([1, 2, 3, 4, 5], 2), [1.5, 3.5, 5.0])
        self.assertEqual(get_averages([1, 2, 3, 4, 5, 6, 7], 3), [2.0, 5.0, 7.0])

        self.assertEqual(get_averages([1000, 2000, 3000, 4000, 5000], 2), [1500.0, 3500.0, 5000.0])
        self.assertEqual(get_averages([1, 2, 3, 4], 5), [2.5])

    def test_make_monotonic(self):
        list0 = []
        list1 = [1]
        list2 = [1, 2, 3, 4]
        list3 = [1, 2, 3, 4, 3, 6, 6, 3]

        self.assertEqual(make_monotonic(list0, MonotonicDirections.INCREASING), [])
        self.assertEqual(make_monotonic(list1, MonotonicDirections.INCREASING), [1])
        self.assertEqual(make_monotonic(list2, MonotonicDirections.INCREASING), [1, 2, 3, 4])
        self.assertEqual(make_monotonic(list3, MonotonicDirections.INCREASING), [1, 2, 3, 4, 4, 6, 6, 6])

        list4 = [1]
        list5 = [4, 3, 2, 1]
        list6 = [3, 6, 6, 3, 4, 3, 2, 1]

        self.assertEqual(make_monotonic(list4, MonotonicDirections.DECREASING), [1])
        self.assertEqual(make_monotonic(list5, MonotonicDirections.DECREASING), [4, 3, 2, 1])
        self.assertEqual(make_monotonic(list6, MonotonicDirections.DECREASING), [6, 6, 6, 4, 4, 3, 2, 1])

    def test_all_zeros(self):
        self.assertEqual(all_zeros([0, 0, 0]), True)
        self.assertEqual(all_zeros([0, 0, 1]), False)
        self.assertEqual(all_zeros([]), True)

    def test_combine_dicts(self):
        # both dicts empty
        dict1 = {}
        dict2 = {}
        expected = {}
        result = combine_dicts(dict1, dict2)
        self.assertEqual(result, expected)

        # 1 dict empty
        dict1 = {}
        dict2 = {"a": [1, 2], "b": [3]}
        expected = {"a": [1, 2], "b": [3]}
        result = combine_dicts(dict1, dict2)
        self.assertEqual(result, expected)

        # other dict empty
        dict1 = {"a": [1, 2], "b": [3]}
        dict2 = {}
        expected = {"a": [1, 2], "b": [3]}
        result = combine_dicts(dict1, dict2)
        self.assertEqual(result, expected)

        # no shared keys
        dict1 = {"a": [1, 2]}
        dict2 = {"b": [3, 4]}
        expected = {"a": [1, 2], "b": [3, 4]}
        result = combine_dicts(dict1, dict2)
        self.assertEqual(result, expected)

        # shared key
        dict1 = {"a": [1, 2]}
        dict2 = {"a": [3, 4]}
        expected = {"a": [1, 2, 3, 4]}
        result = combine_dicts(dict1, dict2)
        self.assertEqual(result, expected)

        # shared key and value
        dict1 = {"a": [1, 2]}
        dict2 = {"a": [2, 3]}
        expected = {"a": [1, 2, 3]}
        result = combine_dicts(dict1, dict2)
        self.assertEqual(result, expected)

        dict1 = {"a": [1, 2], "b": [4, 5]}
        dict2 = {"a": [2, 3], "c": [6]}
        expected = {"a": [1, 2, 3], "b": [4, 5], "c": [6]}
        result = combine_dicts(dict1, dict2)
        self.assertEqual(result, expected)

        dict1 = {"a": [1, 2], "A": [3, 4]}
        dict2 = {"a": [2, 5], "b": [6]}
        expected = {"a": [1, 2, 5], "A": [3, 4], "b": [6]}
        result = combine_dicts(dict1, dict2)
        self.assertEqual(result, expected)

    def test_parse_start_time(self):
        default_start_date = datetime(2024, 1, 1, tzinfo=pytz.utc)
        query_params = {"startdate": '"2024-08-11T12:34:56.789Z"'}
        expected_date = datetime(2024, 8, 11, 12, 34, 56, 789000, tzinfo=pytz.utc)

        result = parse_start_time(query_params, default_start_date)
        self.assertEqual(result, expected_date)

        query_params = {}
        expected_date = default_start_date

        result = parse_start_time(query_params, default_start_date)
        self.assertEqual(result, default_start_date)
