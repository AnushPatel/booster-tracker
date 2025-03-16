from booster_tracker.tasks import update_cached_stageandrecovery_value_task
from booster_tracker.tasks import update_cached_stageandrecovery_value_task, update_launch_times, update_launch_outcome
from booster_tracker.models import (
    StageAndRecovery,
    Launch,
)

from .test_helpers import initialize_test_data
from django.test import TestCase
from django.conf import settings
from datetime import datetime, timedelta
from unittest import mock
import pytz


class TestCases(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_updated_cached_stageandrecovery_value_task(self):
        launch2 = Launch.objects.get(name="Falcon 9 Launch 2")
        temp_launch = Launch.objects.create(
            time=datetime(2024, 3, 1, tzinfo=pytz.utc),
            pad=self.test_data["slc40"],
            rocket=self.test_data["falcon_9"],
            name="Falcon 9 Temp Launch 1",
            orbit=self.test_data["low_earth_orbit"],
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        stage_and_recovery = StageAndRecovery.objects.get(launch=self.test_data["launch2"])
        stage_and_recovery2 = StageAndRecovery.objects.create(
            launch=temp_launch,
            stage=self.test_data["b1062"],
            landing_zone=self.test_data["lz1"],
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        update_cached_stageandrecovery_value_task([stage_and_recovery.stage.id], [stage_and_recovery.landing_zone.id])
        stage_and_recovery.refresh_from_db()
        stage_and_recovery2.refresh_from_db()
        launch2.refresh_from_db()
        temp_launch.refresh_from_db()

        # Check initial launch values
        self.assertEqual(launch2.stages_string, "B1062-2")
        self.assertFalse(stage_and_recovery._from_task)
        self.assertEqual(stage_and_recovery.stage_turnaround, 2678400)
        self.assertEqual(stage_and_recovery.zone_turnaround, 2678400)
        self.assertEqual(stage_and_recovery.num_flights, 2)
        self.assertEqual(stage_and_recovery.num_recoveries, 2)

        self.assertEqual(temp_launch.stages_string, "B1062-3")
        self.assertFalse(stage_and_recovery2._from_task)
        self.assertEqual(stage_and_recovery2.stage_turnaround, 2505600)
        self.assertEqual(stage_and_recovery2.zone_turnaround, 2505600)
        self.assertEqual(stage_and_recovery2.num_flights, 3)
        self.assertEqual(stage_and_recovery2.num_recoveries, 4)

        # Update stage and recovery
        stage_and_recovery.stage = self.test_data["b1080"]
        stage_and_recovery.save(update_fields=["stage"])
        update_cached_stageandrecovery_value_task([stage_and_recovery.stage.id], [stage_and_recovery.landing_zone.id])
        update_cached_stageandrecovery_value_task([self.test_data["b1062"].id], [stage_and_recovery.landing_zone.id])
        stage_and_recovery.refresh_from_db()
        stage_and_recovery2.refresh_from_db()
        launch2.refresh_from_db()
        temp_launch.refresh_from_db()

        self.assertEqual(launch2.stages_string, "B1080-1")
        self.assertFalse(stage_and_recovery._from_task)
        self.assertIsNone(stage_and_recovery.stage_turnaround)
        self.assertEqual(stage_and_recovery.zone_turnaround, 2678400)
        self.assertEqual(stage_and_recovery.num_flights, 1)
        self.assertEqual(stage_and_recovery.num_recoveries, 2)

        self.assertEqual(temp_launch.stages_string, "B1062-2")
        self.assertFalse(stage_and_recovery2._from_task)
        self.assertEqual(stage_and_recovery2.stage_turnaround, 5184000)
        self.assertEqual(stage_and_recovery2.zone_turnaround, 2505600)
        self.assertEqual(stage_and_recovery2.num_flights, 2)
        self.assertEqual(stage_and_recovery2.num_recoveries, 4)

    @mock.patch("booster_tracker.tasks.fetch_nxsf_launches")
    @mock.patch("booster_tracker.tasks.make_x_post")
    def test_post_on_x_task(self, mock_make_x_post, mock_fetch_nxsf_launches):
        temp_launch = Launch.objects.create(
            time=datetime.now(pytz.utc) + timedelta(hours=2),
            pad=self.test_data["slc40"],
            rocket=self.test_data["falcon_9"],
            name="Falcon 9 Temp Launch 10",
            orbit=self.test_data["low_earth_orbit"],
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        temp_launch.x_post_sent = True
        temp_launch.save()

        mock_make_x_post.assert_not_called()

        mock_fetch_nxsf_launches.return_value = []
        mock_make_x_post.assert_not_called()

        nxsf_launch = {"n": temp_launch.name, "t": (temp_launch.time + timedelta(minutes=10)).isoformat()}
        mock_fetch_nxsf_launches.return_value = [nxsf_launch]

        post_string = "This is a test X post."
        mock_make_x_post.side_effect = post_string

    @mock.patch("booster_tracker.tasks.fetch_nxsf_launches")
    def test_updated_launch_times_task(self, mock_fetch_nxsf_launches):
        tomorrow = datetime.now(pytz.utc) + timedelta(days=1)
        test_launch = Launch.objects.create(
            time=tomorrow,
            pad=self.test_data["slc40"],
            rocket=self.test_data["falcon_9"],
            name="Falcon 9 Test Launch",
            orbit=self.test_data["low_earth_orbit"],
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        mock_fetch_nxsf_launches.return_value = [
            {
                "n": test_launch.name,
                "t": (test_launch.time - timedelta(minutes=10)).isoformat(),
                "l": 1,  # Checks for SpaceX
                "s": 4,  # Checks for Scubs
            }
        ]
        update_launch_times()
        test_launch.refresh_from_db()
        expected_date = datetime.now(pytz.utc).date() + timedelta(days=1)
        self.assertEqual(test_launch.time.date(), expected_date)

        current_time = test_launch.time
        new_time = tomorrow + timedelta(hours=2)

        mock_fetch_nxsf_launches.return_value = [
            {
                "n": test_launch.name,
                "t": new_time.isoformat(),
                "l": 1,
                "s": 1,
            }
        ]
        update_launch_times()
        test_launch.refresh_from_db()
        self.assertEqual(test_launch.time, new_time)
        self.assertNotEqual(test_launch.time, current_time)

        test_launch.x_post_sent = True
        test_launch.save()

        new_time = test_launch.time + timedelta(hours=21)

        mock_fetch_nxsf_launches.return_value = [
            {
                "n": test_launch.name,
                "t": new_time.isoformat(),
                "l": 1,
                "s": 1,
            }
        ]

        update_launch_times()
        test_launch.refresh_from_db()

        self.assertEqual(test_launch.time, new_time)
        self.assertFalse(test_launch.x_post_sent)

    @mock.patch("booster_tracker.tasks.fetch_nxsf_launches")
    def test_update_launch_outcome_success(self, mock_fetch_nxsf_launches):
        test_launch = Launch.objects.create(
            time=datetime.now(pytz.utc) - timedelta(hours=1),
            pad=self.test_data["slc40"],
            rocket=self.test_data["falcon_9"],
            name="Falcon 9 Test Launch",
            orbit=self.test_data["low_earth_orbit"],
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        nxsf_data = [
            {
                "n": test_launch.name,
                "t": test_launch.time.isoformat(),
                "l": 1,
                "s": 6,
            }
        ]
        mock_fetch_nxsf_launches.return_value = nxsf_data
        update_launch_outcome()
        test_launch.refresh_from_db()
        self.assertEqual(test_launch.launch_outcome, "SUCCESS")

    @mock.patch("booster_tracker.tasks.fetch_nxsf_launches")
    def test_update_launch_outcome_partial_failure(self, mock_fetch_nxsf_launches):
        test_launch = Launch.objects.create(
            time=datetime.now(pytz.utc) - timedelta(hours=1),
            pad=self.test_data["slc40"],
            rocket=self.test_data["falcon_9"],
            name="Falcon 9 Test Launch",
            orbit=self.test_data["low_earth_orbit"],
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        nxsf_data = [
            {
                "n": test_launch.name,
                "t": test_launch.time.isoformat(),
                "l": 1,
                "s": 7,
            }
        ]
        mock_fetch_nxsf_launches.return_value = nxsf_data
        update_launch_outcome()
        test_launch.refresh_from_db()
        self.assertEqual(test_launch.launch_outcome, "PARTIAL FAILURE")

    @mock.patch("booster_tracker.tasks.fetch_nxsf_launches")
    def test_update_launch_outcome_failure(self, mock_fetch_nxsf_launches):
        test_launch = Launch.objects.create(
            time=datetime.now(pytz.utc) - timedelta(hours=1),
            pad=self.test_data["slc40"],
            rocket=self.test_data["falcon_9"],
            name="Falcon 9 Test Launch",
            orbit=self.test_data["low_earth_orbit"],
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        nxsf_data = [
            {
                "n": test_launch.name,
                "t": test_launch.time.isoformat(),
                "l": 1,
                "s": 8,
            }
        ]
        mock_fetch_nxsf_launches.return_value = nxsf_data
        update_launch_outcome()
        test_launch.refresh_from_db()
        self.assertEqual(test_launch.launch_outcome, "FAILURE")
