from booster_tracker.models import Rocket, Pad, Orbit, Launch, Stage, RocketFamily, StageAndRecovery, LandingZone

from .test_helpers import initialize_test_data
from django.test import TestCase
from datetime import datetime
import pytz
import numpy as np
from scipy.integrate import quad


from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from booster_tracker.models import Launch, Spacecraft, SpacecraftFamily, FairingRecovery
from booster_tracker.api_views import StandardPagination
from booster_tracker.serializers import CalendarStatsSerializer
import json


class FilteredLaunchDaysApiViewTest(APITestCase):
    def setUp(self):
        self.test_data = initialize_test_data()
        self.f9 = Rocket.objects.get(name="Falcon 9")
        self.fh = Rocket.objects.get(name="Falcon Heavy")
        self.client = APIClient()
        self.url = reverse("booster_tracker:filter_calendar_stats")

    def test_filtered_launch_days(self):
        filter_data = {"rocket": {str(self.f9.id): True, str(self.fh.id): True}}
        response = self.client.get(self.url, {"filter": json.dumps(filter_data)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Instead of accessing serializer.data in the test, use initial_data
        response_data = response.json()

        # Add further assertions to check if the response data is correct
        self.assertEqual(response_data["numDaysWithLaunches"], 5)
        self.assertEqual(response_data["percentageDaysWithLaunches"], 1.37)
        self.assertEqual(response_data["mostLaunches"], 1)
        self.assertEqual(
            response_data["daysWithMostLaunches"], "May 01, April 01, March 01, February 01, and January 01"
        )

        Launch.objects.create(
            time=datetime(2022, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        response = self.client.get(self.url, {"filter": json.dumps(filter_data)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Instead of accessing serializer.data in the test, use initial_data
        response_data = response.json()

        # Add further assertions to check if the response data is correct
        self.assertEqual(response_data["numDaysWithLaunches"], 5)
        self.assertEqual(response_data["percentageDaysWithLaunches"], 1.37)
        self.assertEqual(response_data["mostLaunches"], 2)
        self.assertEqual(response_data["daysWithMostLaunches"], "January 01")


class ListApiTestCases(APITestCase):
    def setUp(self):
        self.test_data = initialize_test_data()
        self.f9 = Rocket.objects.get(name="Falcon 9")
        self.fh = Rocket.objects.get(name="Falcon Heavy")
        self.client = APIClient()

    def test_filtered_launches(self):
        # Initial request without filter
        self.url = reverse("booster_tracker:launches")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 4)

        # Filter data
        filter_data = {"rocket": {str(self.f9.id): True, str(self.fh.id): False}}
        response = self.client.get(self.url, {"filter": json.dumps(filter_data)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 4)

        # Adding another launch for verification
        Launch.objects.create(
            time=datetime(2025, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Request with filter after adding another launch
        response = self.client.get(self.url, {"filter": json.dumps(filter_data)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 4)

    def test_filtered_pads(self):
        self.url = reverse("booster_tracker:pads")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Filter data
        filter_data = {}
        response = self.client.get(self.url, {"filter": json.dumps(filter_data)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 2)

    def test_filtered_landing_zones(self):
        self.url = reverse("booster_tracker:landing_zones")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Filter data
        filter_data = {}
        response = self.client.get(self.url, {"filter": json.dumps(filter_data)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data), 3)

    def test_filtered_stages(self):
        filter_data = {"rocket": {str(self.f9.id): True, str(self.fh.id): True}}
        self.url = reverse("booster_tracker:stages")
        response = self.client.get(
            self.url, {"filter": json.dumps(filter_data), "query": "", "type": "BOOSTER", "family": "Falcon"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Filter data
        response = self.client.get(
            self.url, {"filter": json.dumps(filter_data), "query": "", "type": "BOOSTER", "family": "Falcon"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data["stages"]), 3)

    def test_filtered_spacecraft(self):
        filter_data = {}
        self.url = reverse("booster_tracker:spacecraft")
        response = self.client.get(self.url, {"filter": json.dumps(filter_data), "query": "", "family": "dragon"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Filter data
        response = self.client.get(self.url, {"filter": json.dumps(filter_data), "query": "", "family": "dragon"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(len(response_data["spacecraft"]), 0)

    def test_launch_information_view(self):
        launch = Launch.objects.get(name="Falcon 9 Launch 1")
        # Make the GET request to the view
        self.url = reverse("booster_tracker:launch_information")
        response = self.client.get(self.url, {"id": json.dumps(launch.id)})

        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Deserialize the response data
        response_data = response.json()

        self.assertEqual(response_data["name"], launch.name)
        self.assertEqual(response_data["rocket"], launch.rocket.id)
        self.assertEqual(response_data["image"], launch.image)

    def test_landing_zone_information_view(self):
        zone = LandingZone.objects.get(name="Landing Zone 1")
        self.url = reverse("booster_tracker:landing_zone_information")
        response = self.client.get(self.url, {"id": zone.id})

        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Deserialize the response data
        response_data = response.json()

        # Check the response data
        self.assertEqual(response_data["landing_zone"]["id"], zone.id)
        self.assertEqual(len(response_data["stage_and_recoveries"]), 4)
        self.assertEqual(response_data["stage_and_recoveries"][0]["landing_zone"], zone.id)

    def test_stage_information_view(self):
        stage = Stage.objects.get(name="B1062")
        self.url = reverse("booster_tracker:stage_information")
        response = self.client.get(self.url, {"id": stage.id})

        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Deserialize the response data
        response_data = response.json()

        # Check the response data
        self.assertEqual(response_data["stage"]["id"], stage.id)
        self.assertEqual(len(response_data["stage_and_recoveries"]), 3)
        self.assertEqual(response_data["stage_and_recoveries"][0]["stage"], stage.id)

    def test_spacecraft_information_view(self):
        spacecraft_family = SpacecraftFamily.objects.get(name="Dragon")
        spacecraft = Spacecraft.objects.create(family=spacecraft_family, name="C207")
        self.url = reverse("booster_tracker:spacecraft_information")
        response = self.client.get(self.url, {"id": spacecraft.id})

        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Deserialize the response data
        response_data = response.json()

        # Check the response data
        self.assertEqual(response_data["spacecraft"]["id"], spacecraft.id)
        self.assertEqual(len(response_data["spacecraft_on_launches"]), 0)

    def test_pad_information_view(self):
        pad = Pad.objects.get(name="Space Launch Complex 40")
        self.url = reverse("booster_tracker:pad_information")
        response = self.client.get(self.url, {"id": pad.id})

        # Check the status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Deserialize the response data
        response_data = response.json()

        # Check the response data
        self.assertEqual(response_data["pad"]["id"], pad.id)
        self.assertEqual(len(response_data["launches"]), 5)
        self.assertEqual(response_data["launches"][0]["pad"], pad.id)


class HomeDataApiViewTests(APITestCase):
    def setUp(self):
        self.test_data = initialize_test_data()
        self.start_date = "2026-01-01T07:00:00.000Z"
        self.url = reverse("booster_tracker:home")  # Adjust the URL name accordingly

    def test_no_launches(self):
        # Test case where there are no launches
        response = self.client.get(self.url, {"startdate": self.start_date, "functiontype": "exponential"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["turnaround_x_values"], [])
        self.assertEqual(data["turnaround_data"], [])
        self.assertEqual(data["best_fit_turnaround_values"], [])
        self.assertEqual(data["total_launches_current_year"], 0)
        self.assertEqual(data["total_launches_next_year"], 0)

    def test_with_launches(self):
        self.start_date = "2018-01-01T07:00:00.000Z"

        response = self.client.get(self.url, {"startdate": self.start_date, "functiontype": "exponential"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data["turnaround_x_values"], [0.0, 1.0, 2.0, 3.0])
        self.assertEqual(data["turnaround_data"], [31.0, None, 31.0, None])
        np.testing.assert_array_almost_equal(
            data["best_fit_turnaround_values"], [30.42, 30.42, 30.42, 30.42], decimal=0
        )
        self.assertEqual(data["total_launches_current_year"], 10)
        self.assertEqual(data["total_launches_next_year"], 13)


class FamilyInformationApiViewTests(APITestCase):
    def setUp(self):
        # Create test data
        self.test_data = initialize_test_data()
        self.url = reverse("booster_tracker:family_information")

    def test_get_family_information(self):
        response = self.client.get(self.url, {"family_name": "Falcon"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        # Example assertion: Check series_data
        expected_series_data = {
            "Max Booster": [3.0],
            "Avg Booster": [1.86],
        }
        self.assertEqual(data["series_data"], expected_series_data)

        # Example assertion: Check stats
        expected_stats = {
            "Missions": "5",
            "Landings": "6",
            "Reuses": "4",
        }
        self.assertEqual(data["stats"], expected_stats)

        # Example assertion: Check children_stats
        expected_children_stats = {
            "Falcon 9": "{'Launches': '4', 'Successes': '4', 'Booster Reflights': '2', "
            "'2nd Stage Reflights': '0', 'Flight Proven Launches': '2'}",
            "Falcon Heavy": "{'Launches': '1', 'Successes': '1', 'Booster Reflights': "
            "'2', '2nd Stage Reflights': '0', 'Flight Proven Launches': "
            "'1'}",
        }

        self.assertEqual(data["children_stats"], expected_children_stats)
