from booster_tracker.tasks import update_cached_stageandrecovery_value_task

from booster_tracker.models import (
    StageAndRecovery,
    Launch,
)

from .test_helpers import initialize_test_data
from django.test import TestCase
from datetime import datetime
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
