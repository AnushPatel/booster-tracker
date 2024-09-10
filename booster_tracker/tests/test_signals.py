from datetime import datetime, timedelta
from unittest import mock
import pytz
from django.test import TestCase
from django.utils.timezone import now
from booster_tracker.models import StageAndRecovery, SpacecraftOnLaunch, Launch, Stage, Spacecraft
from .test_helpers import initialize_test_data
from celery import current_app
from booster_tracker.tasks import (
    update_cached_stageandrecovery_value_task,
    update_cached_spacecraftonlaunch_value_task,
    post_on_x,
)


class SignalTests(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    @mock.patch("booster_tracker.tasks.update_cached_stageandrecovery_value_task.delay")
    def test_pre_save_signal_caches_old_values(self, mock_update_cached_stageandrecovery_value_task):
        stage_and_recovery = self.test_data["launch1_sr"]
        old_stage_id = stage_and_recovery.stage.id
        old_landing_zone_id = stage_and_recovery.landing_zone.id

        new_stage = Stage.objects.create(
            name="B1050",
            rocket=self.test_data["falcon_9"],
            version="v1.2 Block 5.4",
            type="BOOSTER",
            status="ACTIVE",
        )
        stage_and_recovery.stage = new_stage
        stage_and_recovery.save()

        # ensure that the pre_save is working
        self.assertEqual(stage_and_recovery._old_stage_id, old_stage_id)
        self.assertEqual(stage_and_recovery._old_landing_zone_id, old_landing_zone_id)
        self.assertEqual(stage_and_recovery.stage.id, new_stage.id)

        # ensure that the stage_and_recovery save makes the correct method call
        mock_update_cached_stageandrecovery_value_task.assert_called_once_with(
            [stage_and_recovery.stage.id, old_stage_id], [stage_and_recovery.landing_zone.id, old_landing_zone_id]
        )

        # ensure post_delete receiver is working
        stage_and_recovery.delete()
        self.assertEqual(mock_update_cached_stageandrecovery_value_task.call_count, 2)
        mock_update_cached_stageandrecovery_value_task.assert_has_calls(
            [
                mock.call(
                    [stage_and_recovery.stage.id, old_stage_id],
                    [stage_and_recovery.landing_zone.id, old_landing_zone_id],
                ),
                mock.call(
                    [stage_and_recovery.stage.id, old_stage_id],
                    [stage_and_recovery.landing_zone.id, old_landing_zone_id],
                ),
            ]
        )

    @mock.patch("booster_tracker.tasks.update_cached_spacecraftonlaunch_value_task.delay")
    def test_pre_save_signal_caches_old_spacecraft_id(self, mock_update_cached_spacecraftonlaunch_value_task):
        # Create objects for test
        temp_launch = Launch.objects.create(
            time=datetime(2024, 3, 1, tzinfo=pytz.utc),
            pad=self.test_data["slc40"],
            rocket=self.test_data["falcon_9"],
            name="Falcon 9 Temp Launch 2",
            orbit=self.test_data["low_earth_orbit"],
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )
        spacecraft_on_launch = SpacecraftOnLaunch.objects.create(
            launch=temp_launch,
            spacecraft=self.test_data["c206"],
        )

        old_spacecraft_id = spacecraft_on_launch.spacecraft.id

        # Update launch value
        spacecraft_on_launch.spacecraft = self.test_data["c207"]
        spacecraft_on_launch.save()

        # Ensure spacecraft ID is correct; and that two receiver signals have been received (one for creation, one for update)
        self.assertEqual(spacecraft_on_launch._old_spacecraft_id, old_spacecraft_id)
        self.assertEqual(spacecraft_on_launch.spacecraft.id, self.test_data["c207"].id)
        self.assertEqual(mock_update_cached_spacecraftonlaunch_value_task.call_count, 2)
        mock_update_cached_spacecraftonlaunch_value_task.assert_has_calls(
            [
                mock.call(
                    [old_spacecraft_id],
                ),
                mock.call(
                    [old_spacecraft_id, spacecraft_on_launch.spacecraft.id],
                ),
            ]
        )

        # Ensure deletion behavior works as expected
        spacecraft_on_launch.delete()
        self.assertEqual(mock_update_cached_spacecraftonlaunch_value_task.call_count, 3)
        mock_update_cached_spacecraftonlaunch_value_task.assert_has_calls(
            [
                mock.call(
                    [old_spacecraft_id],
                ),
                mock.call(
                    [old_spacecraft_id, spacecraft_on_launch.spacecraft.id],
                ),
                mock.call(
                    [old_spacecraft_id, spacecraft_on_launch.spacecraft.id],
                ),
            ]
        )

    def setUp(self):
        self.test_data = initialize_test_data()
        self.time = datetime.now(pytz.utc)
        self.temp_launch = Launch.objects.create(
            time=self.time,
            pad=self.test_data["slc40"],
            rocket=self.test_data["falcon_9"],
            name="Falcon 9 Temp Launch 1",
            orbit=self.test_data["low_earth_orbit"],
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
            x_post_sent=False,
            celery_task_id=None,
        )

    @mock.patch("celery.current_app.control.revoke")
    @mock.patch("booster_tracker.tasks.post_on_x.apply_async")
    @mock.patch("booster_tracker.tasks.update_cached_launch_value_task.delay")
    def test_post_save_signal_triggers_cache_update(
        self, mock_update_cached_launch_value_task, mock_apply_async, mock_revoke
    ):
        original_time = self.temp_launch.time
        celery_id = self.temp_launch.celery_task_id

        mock_apply_async.return_value.id = "1"
        self.temp_launch.time = self.time + timedelta(hours=3)
        self.temp_launch.save()

        self.assertEqual(self.temp_launch._original_time, original_time)
        self.temp_launch.save()
        self.assertEqual(mock_update_cached_launch_value_task.call_count, 2)

        self.temp_launch.time = self.time + timedelta(hours=3)
        self.temp_launch.save()

        # Verify task scheduling
        post_time = self.temp_launch.time - timedelta(minutes=15)
        self.assertEqual(mock_update_cached_launch_value_task.call_count, 3)

        mock_apply_async.assert_called_once_with((self.temp_launch.id,), eta=post_time)

        # Verify task revocation if it existed
        self.assertTrue(mock_revoke.called)

        self.temp_launch.celery_task_id = "some-task-id"
        self.temp_launch.save()
        self.temp_launch.delete()

        # Check that the task was revoked
        mock_revoke.assert_has_calls([mock.call(celery_id, terminate=True), mock.call("some-task-id", terminate=True)])
