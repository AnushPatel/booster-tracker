from django.test import TestCase
from .test_helpers import initialize_test_data
from booster_tracker.models import (
    Operator,
    Rocket,
    Pad,
    Orbit,
    Boat,
    LandingZone,
    Stage,
    PadUsed,
    StageAndRecovery,
    Launch,
    RocketFamily,
)
from booster_tracker.utils import TurnaroundObjects
from datetime import datetime
import pytz


class TestCases(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_num_launches_rocket(self):
        # Test function on perm objects
        self.assertEqual(Rocket.objects.get(name="Falcon 9").num_launches, 4)
        self.assertEqual(Rocket.objects.get(name="Falcon Heavy").num_launches, 1)

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="FAILURE",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Test function on response to additional launch
        self.assertEqual(Rocket.objects.get(name="Falcon 9").num_launches, 5)
        self.assertEqual(Rocket.objects.get(name="Falcon Heavy").num_launches, 2)

    def test_num_successes(self):
        # Test function on perm objects
        self.assertEqual(Rocket.objects.get(name="Falcon 9").num_successes, 4)
        self.assertEqual(Rocket.objects.get(name="Falcon Heavy").num_successes, 1)

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="FAILURE",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Test function on additional launches
        self.assertEqual(Rocket.objects.get(name="Falcon 9").num_successes, 4)
        self.assertEqual(Rocket.objects.get(name="Falcon Heavy").num_successes, 2)

    # Test the methods for pads and landing zones
    def test_num_launches(self):
        # Test number of launches and landings on perm objects
        self.assertEqual(Pad.objects.get(nickname="SLC-40").num_launches, 5)
        self.assertEqual(Pad.objects.get(nickname="LC-39A").num_launches, 0)

        self.assertEqual(LandingZone.objects.get(nickname="LZ-1").num_landings, 4)
        self.assertEqual(LandingZone.objects.get(nickname="LZ-2").num_landings, 1)
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").num_landings, 2)

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Following the addition of launches from new pad, ensure functions update accordingly
        self.assertEqual(Pad.objects.get(nickname="SLC-40").num_launches, 5)
        self.assertEqual(Pad.objects.get(nickname="LC-39A").num_launches, 1)

        self.assertEqual(LandingZone.objects.get(nickname="LZ-1").num_landings, 4)
        self.assertEqual(LandingZone.objects.get(nickname="LZ-2").num_landings, 2)
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").num_landings, 2)

        Launch.objects.create(
            time=datetime(2024, 4, 2, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Following the addition of another alunch, ensure other landing zone updates accordingly
        self.assertEqual(Pad.objects.get(nickname="SLC-40").num_launches, 5)
        self.assertEqual(Pad.objects.get(nickname="LC-39A").num_launches, 2)

        self.assertEqual(LandingZone.objects.get(nickname="LZ-1").num_landings, 5)
        self.assertEqual(LandingZone.objects.get(nickname="LZ-2").num_landings, 2)
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").num_landings, 2)

    def test_fastest_turnaround(self):
        # Test with perm objects
        self.assertEqual(Pad.objects.get(nickname="SLC-40").fastest_turnaround, "29 days")
        self.assertEqual(Pad.objects.get(nickname="LC-39A").fastest_turnaround, "N/A")

        self.assertEqual(LandingZone.objects.get(nickname="LZ-1").fastest_turnaround, "29 days")
        self.assertEqual(LandingZone.objects.get(nickname="LZ-2").fastest_turnaround, "N/A")
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").fastest_turnaround, "30 days")

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Ensure after adding launch that is not new quickest does not update
        self.assertEqual(Pad.objects.get(nickname="SLC-40").fastest_turnaround, "29 days")
        self.assertEqual(Pad.objects.get(nickname="LC-39A").fastest_turnaround, "N/A")

        self.assertEqual(LandingZone.objects.get(nickname="LZ-1").fastest_turnaround, "29 days")
        self.assertEqual(LandingZone.objects.get(nickname="LZ-2").fastest_turnaround, "N/A")
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").fastest_turnaround, "30 days")

        Launch.objects.create(
            time=datetime(2024, 4, 2, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Ensure stats update correctly with new quickest turnaround
        self.assertEqual(Pad.objects.get(nickname="SLC-40").fastest_turnaround, "29 days")
        self.assertEqual(Pad.objects.get(nickname="LC-39A").fastest_turnaround, "1 day")

        self.assertEqual(LandingZone.objects.get(nickname="LZ-1").fastest_turnaround, "1 day")
        self.assertEqual(LandingZone.objects.get(nickname="LZ-2").fastest_turnaround, "N/A")
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").fastest_turnaround, "30 days")

        self.assertEqual(Stage.objects.get(name="B1062").fastest_turnaround, "31 days")

    # And now test functions in models.py
    def test_droneship_needed(self):
        # Test perm launch objects
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").droneship_needed, False)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").droneship_needed, False)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").droneship_needed, True)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").droneship_needed, False)

    def test_flight_proven_booster(self):
        # Test perm stage and recoveries
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").flight_proven_booster, False)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").flight_proven_booster, True)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").flight_proven_booster, True)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").flight_proven_booster, True)

        Stage.objects.create(
            name="B1000",
            rocket=Rocket.objects.get(name="Falcon 9"),
            version="v1.2 Block 5.4",
            type="BOOSTER",
            status="ACTIVE",
        )
        Stage.objects.create(
            name="B1001",
            rocket=Rocket.objects.get(name="Falcon 9"),
            version="v1.2 Block 5.5",
            type="BOOSTER",
            status="ACTIVE",
        )
        Stage.objects.create(
            name="B1002",
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            version="v1.2 Block 5.5",
            type="BOOSTER",
            status="ACTIVE",
        )

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1000"),
            stage_position="MY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1001"),
            stage_position="PY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1002"),
            stage_position="CENTER",
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Test Falcon Heavy with all new cores passes
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Temp Launch 1").flight_proven_booster,
            False,
        )

    def test_num_successful_landings(self):
        # Test on perm objects
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").num_successful_landings, 1)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").num_successful_landings, 1)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").num_successful_landings, 3)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").num_successful_landings, 0)

    def test_get_stage_flights_and_turnaround(self):
        # Test on perm StageAndRecovery objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").get_stage_flights_and_turnaround(
                stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 1"))
            ),
            (1, None),
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").get_stage_flights_and_turnaround(
                stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 2"))
            ),
            (2, 31.00),
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_stage_flights_and_turnaround(
                stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 3"))
            ),
            (1, None),
        )

        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights_and_turnaround(
                stage=Stage.objects.get(name="B1062")
            ),
            (3, 60.00),
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights_and_turnaround(
                stage=Stage.objects.get(name="B1080")
            ),
            (2, 31.00),
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights_and_turnaround(
                stage=Stage.objects.get(name="B1084")
            ),
            (1, None),
        )

    def test_get_rocket_flights_reused_vehicle(self):
        # Test on perm objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").get_rocket_flights_reused_vehicle(),
            0,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").get_rocket_flights_reused_vehicle(),
            1,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_rocket_flights_reused_vehicle(),
            1,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_rocket_flights_reused_vehicle(),
            1,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").get_rocket_flights_reused_vehicle(),
            2,
        )

        Stage.objects.create(
            name="B1081",
            rocket=Rocket.objects.get(name="Falcon 9"),
            version="v1.2 Block 5.5",
            type="BOOSTER",
            status="ACTIVE",
        )

        Launch.objects.create(
            time=datetime(2024, 6, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 7, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 8, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1081"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage=Stage.objects.get(name="B1081"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1080"),
            stage_position="MY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1062"),
            stage_position="PY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1084"),
            stage_position="CENTER",
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Ensure function updates as expected for Falcon launches with varying number of flight proven boosters
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").get_rocket_flights_reused_vehicle(),
            2,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 2").get_rocket_flights_reused_vehicle(),
            3,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Temp Launch 1").get_rocket_flights_reused_vehicle(),
            2,
        )

    def test_get_total_reflights(self):
        # Just some random date that is before all launches
        past_time = datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc)
        # A time that is between launches to ensure offset works
        later_time = datetime(2024, 2, 2, 0, 0, tzinfo=pytz.utc)
        # Test perm launch objects for all time
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").get_total_reflights(stage_type="BOOSTER", start=past_time),
            [],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").get_total_reflights(stage_type="BOOSTER", start=past_time),
            [1],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_total_reflights(stage_type="BOOSTER", start=past_time),
            [],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_total_reflights(stage_type="BOOSTER", start=past_time),
            [2, 3],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").get_total_reflights(stage_type="BOOSTER", start=past_time),
            [4],
        )

        # later_time is after first launch but before all launches after; ensure that the numbers above drop by one
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_total_reflights(stage_type="BOOSTER", start=later_time),
            [],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_total_reflights(
                stage_type="BOOSTER", start=later_time
            ),
            [1, 2],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").get_total_reflights(stage_type="BOOSTER", start=later_time),
            [3],
        )

    def test_get_num_booster_landings(self):
        # Test on perm launch objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").get_num_stage_landings(stage_type="BOOSTER"),
            [1],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").get_num_stage_landings(stage_type="BOOSTER"),
            [2],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_num_stage_landings(stage_type="BOOSTER"),
            [3],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_num_stage_landings(stage_type="BOOSTER"),
            [4, 5, 6],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").get_num_stage_landings(stage_type="BOOSTER"),
            [],
        )

        Launch.objects.create(
            time=datetime(2024, 6, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
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

        # Ensure function responds accordingly
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").get_num_stage_landings(stage_type="BOOSTER"),
            [7],
        )

    def test_calculate_turnarounds(self):
        # Test perm launch objects
        # Start by testing the ALL case
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(turnaround_object=TurnaroundObjects.ALL),
            None,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(turnaround_object=TurnaroundObjects.ALL),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    }
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(turnaround_object=TurnaroundObjects.ALL),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.ALL
            ),
            {
                "is_record": False,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(turnaround_object=TurnaroundObjects.ALL),
            {
                "is_record": False,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2592000.0,
                        "launch_name": "Falcon 9 Launch 4",
                        "last_launch_name": "Falcon Heavy Launch 1",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )

        # Testing of BOOSTER case
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.BOOSTER
            ),
            None,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.BOOSTER
            ),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Stage.objects.get(name="B1062"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    }
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.BOOSTER
            ),
            {
                "is_record": False,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Stage.objects.get(name="B1062"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    }
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.BOOSTER
            ),
            {
                "is_record": False,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Stage.objects.get(name="B1062"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": Stage.objects.get(name="B1080"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                    {
                        "turnaround_object": Stage.objects.get(name="B1062"),
                        "turnaround_time": 5184000.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.BOOSTER
            ),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Stage.objects.get(name="B1080"),
                        "turnaround_time": 2592000.0,
                        "launch_name": "Falcon 9 Launch 4",
                        "last_launch_name": "Falcon Heavy Launch 1",
                    },
                    {
                        "turnaround_object": Stage.objects.get(name="B1062"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": Stage.objects.get(name="B1080"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                    {
                        "turnaround_object": Stage.objects.get(name="B1062"),
                        "turnaround_time": 5184000.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                ],
            },
        )

        # Testing of PAD case
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(turnaround_object=TurnaroundObjects.PAD),
            None,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(turnaround_object=TurnaroundObjects.PAD),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    }
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(turnaround_object=TurnaroundObjects.PAD),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.PAD
            ),
            {
                "is_record": False,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(turnaround_object=TurnaroundObjects.PAD),
            {
                "is_record": False,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2592000.0,
                        "launch_name": "Falcon 9 Launch 4",
                        "last_launch_name": "Falcon Heavy Launch 1",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Testing of LANDING_ZONE case
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.LANDING_ZONE
            ),
            None,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.LANDING_ZONE
            ),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    }
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.LANDING_ZONE
            ),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.LANDING_ZONE
            ),
            {
                "is_record": False,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.LANDING_ZONE
            ),
            {
                "is_record": False,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": self.test_data["lz1"],
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": self.test_data["jrti"],
                        "turnaround_time": 2592000.0,
                        "launch_name": "Falcon 9 Launch 4",
                        "last_launch_name": "Falcon Heavy Launch 1",
                    },
                    {
                        "turnaround_object": self.test_data["lz1"],
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": self.test_data["lz1"],
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )

        Launch.objects.create(
            time=datetime(2024, 4, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Make sure it responds correctly when another launch is added
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.BOOSTER
            ),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Stage.objects.get(name="B1080"),
                        "turnaround_time": 86400.0,
                        "launch_name": "Falcon 9 Temp Launch 1",
                        "last_launch_name": "Falcon Heavy Launch 1",
                    },
                    {
                        "turnaround_object": Stage.objects.get(name="B1062"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": Stage.objects.get(name="B1080"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                    {
                        "turnaround_object": Stage.objects.get(name="B1062"),
                        "turnaround_time": 5184000.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.PAD
            ),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 86400.0,
                        "launch_name": "Falcon 9 Temp Launch 1",
                        "last_launch_name": "Falcon Heavy Launch 1",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": Pad.objects.get(nickname="SLC-40"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.LANDING_ZONE
            ),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="JRtI"),
                        "turnaround_time": 86400.0,
                        "launch_name": "Falcon 9 Temp Launch 1",
                        "last_launch_name": "Falcon Heavy Launch 1",
                    },
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": LandingZone.objects.get(nickname="LZ-1"),
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.ALL
            ),
            {
                "is_record": True,
                "ordered_turnarounds": [
                    {
                        "turnaround_object": "",
                        "turnaround_time": 86400.0,
                        "launch_name": "Falcon 9 Temp Launch 1",
                        "last_launch_name": "Falcon Heavy Launch 1",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2505600.0,
                        "launch_name": "Falcon 9 Launch 3",
                        "last_launch_name": "Falcon 9 Launch 2",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon 9 Launch 2",
                        "last_launch_name": "Falcon 9 Launch 1",
                    },
                    {
                        "turnaround_object": "",
                        "turnaround_time": 2678400.0,
                        "launch_name": "Falcon Heavy Launch 1",
                        "last_launch_name": "Falcon 9 Launch 3",
                    },
                ],
            },
        )

    def test_get_consec_landings(self):
        # Test on perm launch objects
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").get_consec_landings(stage_type="BOOSTER"), [1])
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").get_consec_landings(stage_type="BOOSTER"), [2])
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").get_consec_landings(stage_type="BOOSTER"), [3])
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_consec_landings(stage_type="BOOSTER"),
            [4, 5, 6],
        )
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").get_consec_landings(stage_type="BOOSTER"), [])

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="FAILURE",
            recovery_success=True,
        )

        # Ensure a landing failure resets count
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").get_consec_landings(stage_type="BOOSTER"),
            [],
        )

        Launch.objects.create(
            time=datetime(2024, 5, 3, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Ensure landing after failure is 1st success
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 2").get_consec_landings(stage_type="BOOSTER"),
            [1],
        )

        Launch.objects.create(
            time=datetime(2024, 5, 4, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1062"),
            stage_position="MY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="FAILURE",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1080"),
            stage_position="PY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1084"),
            stage_position="CENTER",
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Ensure FH with booster that fails to land first resets as expected
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Temp Launch 1").get_consec_landings(stage_type="BOOSTER"),
            [1, 2],
        )

        Launch.objects.create(
            time=datetime(2024, 5, 5, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 2"),
            stage=Stage.objects.get(name="B1062"),
            stage_position="MY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 2"),
            stage=Stage.objects.get(name="B1080"),
            stage_position="PY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="FAILURE",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 2"),
            stage=Stage.objects.get(name="B1084"),
            stage_position="CENTER",
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Ensure if middle booster fails to land the function returns 1st
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Temp Launch 2").get_consec_landings(stage_type="BOOSTER"),
            [1],
        )

        Launch.objects.create(
            time=datetime(2024, 5, 6, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 3"),
            stage=Stage.objects.get(name="B1062"),
            stage_position="MY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 3"),
            stage=Stage.objects.get(name="B1080"),
            stage_position="PY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 3"),
            stage=Stage.objects.get(name="B1084"),
            stage_position="CENTER",
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="GROUND_PAD",
            method_success="FAILURE",
            recovery_success=True,
        )

        # Ensure if last booster fails to land the function returns N/A
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Temp Launch 3").get_consec_landings(stage_type="BOOSTER"),
            [],
        )

        today = datetime.now(pytz.utc)
        Launch.objects.create(
            time=datetime(today.year, today.month + 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 3"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            recovery_success=False,
        )

        # Ensure that launch in the future is assumed to have successful landings
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 3").get_consec_landings(stage_type="BOOSTER"),
            [1],
        )

    def test_get_boosters(self):
        # Test for perm objects
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").boosters, "B1062-1")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").boosters, "B1062-2")
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").boosters,
            "B1084-1, B1080-2, and B1062-3",
        )
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").boosters, "B1080-3")

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Ensure launch with no booster assigned gets unknown
        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").boosters, "Unknown")

    def test_get_recoveries(self):
        # Test for perm objects
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").recoveries, "LZ-1")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").recoveries, "LZ-1")
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").recoveries,
            "JRtI, LZ-1, and LZ-2",
        )
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").recoveries, "JRtI")

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Test for when no recovery information added
        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").recoveries, "N/A")

    def test_make_booster_display(self):
        # Test for perm objects; space is intentional for formatting in table
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").make_booster_display(),
            " B1062-1; N/A-day turnaround",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").make_booster_display(),
            " B1062-2; 31.00-day turnaround",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").make_booster_display(),
            " B1084-1, B1080-2, B1062-3; N/A, 31.00, 60.00-day turnaround",
        )

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Test for launch with unknown booster
        self.assertAlmostEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").make_booster_display(),
            "; Unknown booster",
        )

    def test_make_landing_string(self):
        # Test for perm objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").make_landing_string(),
            "B1062 successfully completed a landing on Landing Zone 1 (LZ-1)",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").make_landing_string(),
            "B1062 successfully completed a landing on Landing Zone 1 (LZ-1)",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").make_landing_string(),
            "B1080 successfully completed a landing on Landing Zone 1 (LZ-1)",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").make_landing_string(),
            "B1084 successfully completed a landing on Just Read the Instructions (JRtI); B1080 successfully completed a landing on Landing Zone 1 (LZ-1); B1062 successfully completed a landing on Landing Zone 2 (LZ-2)",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").make_landing_string(),
            "B1080 was expended",
        )

        Launch.objects.create(
            time=datetime(datetime.now(pytz.utc).year, 5, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="OCEAN_SURFACE",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Test for object landing on ocean surface
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").make_landing_string(),
            "B1062 successfully completed a soft landing on the ocean surface",
        )

        Launch.objects.create(
            time=datetime(datetime.now(pytz.utc).year + 1, 5, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="OCEAN_SURFACE",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Test for future landing
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 2").make_landing_string(),
            "B1062 will attempt a soft landing on the ocean surface",
        )

        Launch.objects.create(
            time=datetime(datetime.now(pytz.utc).year + 1, 5, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Test for future expended launch
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 3").make_landing_string(),
            "The stage will be expended",
        )

        Launch.objects.create(
            time=datetime(datetime.now(pytz.utc).year, 5, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 4",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Test for past expended launch
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 4").make_landing_string(),
            "The stage was expended",
        )

    def test_make_stats(self):
        # Test for perm objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").make_stats(),
            [
                (True, "– 1st Falcon 9 mission"),
                (True, "– 1st booster landing"),
                (True, "– 1st consecutive booster landing"),
                (True, "– 1st SpaceX launch of 2024"),
                (True, "– 1st SpaceX launch from SLC-40"),
            ],
        )

        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").make_stats(),
            [
                (False, "– 2nd Falcon 9 mission"),
                (True, "– 1st Falcon 9 flight with a flight-proven booster"),
                (True, "– 1st reflight of a Falcon booster"),
                (True, "– 1st reflight of a Falcon booster in 2024"),
                (False, "– 2nd booster landing"),
                (False, "– 2nd consecutive booster landing"),
                (False, "– 2nd SpaceX launch of 2024"),
                (False, "– 2nd SpaceX launch from SLC-40"),
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").make_stats(),
            [
                (False, "– 3rd Falcon 9 mission"),
                (False, "– 3rd booster landing"),
                (False, "– 3rd consecutive booster landing"),
                (False, "– 3rd SpaceX launch of 2024"),
                (False, "– 3rd SpaceX launch from SLC-40"),
                (True, "– Fastest turnaround of SLC-40 to date at 29 days. Previous record: SLC-40 at 31 days"),
                (True, "– Fastest turnaround of SpaceX to date at 29 days. Previous record: 31 days"),
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").make_stats(),
            [
                (True, "– 1st Falcon Heavy mission"),
                (True, "– 1st Falcon Heavy flight with a flight-proven booster"),
                (False, "– 2nd and 3rd reflight of a Falcon booster"),
                (False, "– 2nd and 3rd reflight of a Falcon booster in 2024"),
                (False, "– 4th, 5th, and 6th booster landings"),
                (False, "– 4th, 5th, and 6th consecutive booster landings"),
                (False, "– 4th SpaceX launch of 2024"),
                (False, "– 4th SpaceX launch from SLC-40"),
            ],
        )

        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").make_stats(),
            [
                (False, "– 4th Falcon 9 mission"),
                (False, "– 2nd Falcon 9 flight with a flight-proven booster"),
                (False, "– 4th reflight of a Falcon booster"),
                (False, "– 4th reflight of a Falcon booster in 2024"),
                (False, "– 5th SpaceX launch of 2024"),
                (False, "– 5th SpaceX launch from SLC-40"),
                (
                    True,
                    "– Fastest turnaround of a Falcon booster to date at 30 days. Previous record: B1062 at 31 days",
                ),
            ],
        )

        Launch.objects.create(
            time=datetime(2024, 5, 1, 0, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Test stats update for additional launch
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").make_stats(),
            [
                (False, "– 5th Falcon 9 mission"),
                (False, "– 3rd Falcon 9 flight with a flight-proven booster"),
                (False, "– 5th reflight of a Falcon booster"),
                (False, "– 5th reflight of a Falcon booster in 2024"),
                (False, "– 7th booster landing"),
                (False, "– 7th consecutive booster landing"),
                (False, "– 6th SpaceX launch of 2024"),
                (False, "– 6th SpaceX launch from SLC-40"),
                (False, "– Fastest turnaround of B1062 to date at 30 days and 1 minute. Previous record: 31 days"),
                (True, "– Fastest turnaround of SLC-40 to date at 1 minute. Previous record: SLC-40 at 29 days"),
                (True, "– Fastest turnaround of SpaceX to date at 1 minute. Previous record: 29 days"),
            ],
        )

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 12, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 3"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Test to ensure quickest turnaround stats work
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 2").make_stats(),
            [
                (False, "– 6th Falcon 9 mission"),
                (False, "– 4th Falcon 9 flight with a flight-proven booster"),
                (False, "– 6th reflight of a Falcon booster"),
                (False, "– 6th reflight of a Falcon booster in 2024"),
                (False, "– 8th booster landing"),
                (False, "– 8th consecutive booster landing"),
                (False, "– 7th SpaceX launch of 2024"),
                (True, "– 1st SpaceX launch from LC-39A"),
                (
                    True,
                    "– Fastest turnaround of a Falcon booster to date at 23 hours and 59 minutes. Previous record: B1080 at 30 days",
                ),
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 3").make_stats(),
            [
                (False, "– 7th Falcon 9 mission"),
                (False, "– 5th Falcon 9 flight with a flight-proven booster"),
                (False, "– 7th reflight of a Falcon booster"),
                (False, "– 7th reflight of a Falcon booster in 2024"),
                (False, "– 9th booster landing"),
                (False, "– 9th consecutive booster landing"),
                (False, "– 8th SpaceX launch of 2024"),
                (False, "– 2nd SpaceX launch from LC-39A"),
            ],
        )

    def test_create_launch_table(self):
        # Test for perm objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").create_launch_table(),
            {
                "Liftoff Time": ["January 01, 2024 - 00:00 UTC", "December 31, 2023 - 19:00 EST"],
                "Mission Name": ["Falcon 9 Launch 1"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1062-1; N/A-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1,000 kg (2,200 lb)"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": ["B1062 successfully completed a landing on Landing Zone 1 (LZ-1)"],
                "Did they attempt to recover the fairings?": ["There are no fairings on this flight"],
                "This was the": [
                    "– 1st Falcon 9 mission",
                    "– 1st booster landing",
                    "– 1st consecutive booster landing",
                    "– 1st SpaceX launch of 2024",
                    "– 1st SpaceX launch from SLC-40",
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").create_launch_table(),
            {
                "Liftoff Time": ["February 01, 2024 - 00:00 UTC", "January 31, 2024 - 19:00 EST"],
                "Mission Name": ["Falcon 9 Launch 2"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1062-2; 31.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1,000 kg (2,200 lb)"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": ["B1062 successfully completed a landing on Landing Zone 1 (LZ-1)"],
                "Did they attempt to recover the fairings?": ["There are no fairings on this flight"],
                "This was the": [
                    "– 1st Falcon 9 flight with a flight-proven booster",
                    "– 1st reflight of a Falcon booster",
                    "– 1st reflight of a Falcon booster in 2024",
                    "– 2nd Falcon 9 mission",
                    "– 2nd booster landing",
                    "– 2nd consecutive booster landing",
                    "– 2nd SpaceX launch of 2024",
                    "– 2nd SpaceX launch from SLC-40",
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").create_launch_table(),
            {
                "Liftoff Time": ["March 01, 2024 - 00:00 UTC", "February 29, 2024 - 19:00 EST"],
                "Mission Name": ["Falcon 9 Launch 3"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1080-1; N/A-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1,000 kg (2,200 lb)"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": ["B1080 successfully completed a landing on Landing Zone 1 (LZ-1)"],
                "Did they attempt to recover the fairings?": ["There are no fairings on this flight"],
                "This was the": [
                    "– Fastest turnaround of SLC-40 to date at 29 days. Previous record: SLC-40 at 31 days",
                    "– Fastest turnaround of SpaceX to date at 29 days. Previous record: 31 days",
                    "– 3rd Falcon 9 mission",
                    "– 3rd booster landing",
                    "– 3rd consecutive booster landing",
                    "– 3rd SpaceX launch of 2024",
                    "– 3rd SpaceX launch from SLC-40",
                ],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").create_launch_table(),
            {
                "Liftoff Time": ["April 01, 2024 - 00:00 UTC", "March 31, 2024 - 20:00 EDT"],
                "Mission Name": ["Falcon Heavy Launch 1"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon Heavy B1084-1, B1080-2, B1062-3; N/A, 31.00, 60.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1,000 kg (2,200 lb)"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": [
                    "B1084 successfully completed a landing on Just Read the Instructions (JRtI); B1080 successfully completed a landing on Landing Zone 1 (LZ-1); B1062 successfully completed a landing on Landing Zone 2 (LZ-2)",
                    "",
                    "Tug: N/A; Support: N/A",
                ],
                "Did they attempt to recover the fairings?": ["There are no fairings on this flight"],
                "This was the": [
                    "– 1st Falcon Heavy mission",
                    "– 1st Falcon Heavy flight with a flight-proven booster",
                    "– 2nd and 3rd reflight of a Falcon booster",
                    "– 2nd and 3rd reflight of a Falcon booster in 2024",
                    "– 4th, 5th, and 6th booster landings",
                    "– 4th, 5th, and 6th consecutive booster landings",
                    "– 4th SpaceX launch of 2024",
                    "– 4th SpaceX launch from SLC-40",
                ],
            },
        )

        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").create_launch_table(),
            {
                "Liftoff Time": ["May 01, 2024 - 00:00 UTC", "April 30, 2024 - 20:00 EDT"],
                "Mission Name": ["Falcon 9 Launch 4"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1080-3; 30.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1,000 kg (2,200 lb)"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": ["B1080 was expended"],
                "Did they attempt to recover the fairings?": ["There are no fairings on this flight"],
                "This was the": [
                    "– Fastest turnaround of a Falcon booster to date at 30 days. Previous record: B1062 at 31 days",
                    "– 4th Falcon 9 mission",
                    "– 2nd Falcon 9 flight with a flight-proven booster",
                    "– 4th reflight of a Falcon booster",
                    "– 4th reflight of a Falcon booster in 2024",
                    "– 5th SpaceX launch of 2024",
                    "– 5th SpaceX launch from SLC-40",
                ],
            },
        )

        Launch.objects.create(
            time=datetime(datetime.now(pytz.utc).year + 1, 5, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="OCEAN_SURFACE",
            method_success="SUCCESS",
            recovery_success=True,
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Test for additional launch that is landing on ocean surface
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").create_launch_table(),
            {
                "Liftoff Time": ["May 01, 2025 - 00:00 UTC", "April 30, 2025 - 20:00 EDT"],
                "Mission Name": ["Falcon 9 Temp Launch 1"],
                "Launch Provider <br /> (What rocket company is launching it?)": ["SpaceX"],
                "Customer <br /> (Who's paying for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1062-4; 395.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1,000 kg (2,200 lb)"],
                "Where are the satellites going?": ["low-Earth Orbit"],
                "Where will the first stage land?": ["B1062 will attempt a soft landing on the ocean surface"],
                "Will they be attempting to recover the fairings?": ["There are no fairings on this flight"],
                "This will be the": [
                    "– 1st reflight of a Falcon booster in 2025",
                    "– 1st SpaceX launch of 2025",
                    "– 5th Falcon 9 mission",
                    "– 3rd Falcon 9 flight with a flight-proven booster",
                    "– 5th reflight of a Falcon booster",
                    "– 6th SpaceX launch from SLC-40",
                ],
            },
        )

        Launch.objects.create(
            time=datetime(2024, 5, 10, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="DRONE_SHIP",
            recovery_success=True,
        )

        for stage_and_recovery in StageAndRecovery.objects.all():
            stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
            stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
            stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
            stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
            stage_and_recovery.save(
                update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"]
            )

        for launch in Launch.objects.all():
            launch.stages_string = launch.boosters
            launch.company_turnaround = launch.get_company_turnaround
            launch.pad_turnaround = launch.get_pad_turnaround
            launch.image = launch.get_image
            launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

        # Test additional launch for drone ship
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 2").create_launch_table(),
            {
                "Liftoff Time": ["May 10, 2024 - 00:00 UTC", "May 09, 2024 - 20:00 EDT"],
                "Mission Name": ["Falcon 9 Temp Launch 2"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1062-4; 39.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1,000 kg (2,200 lb)"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": [
                    "B1062 successfully completed a landing on Landing Zone 1 (LZ-1)",
                    "",
                    "Tug: N/A; Support: N/A",
                ],
                "Did they attempt to recover the fairings?": ["There are no fairings on this flight"],
                "This was the": [
                    "– Fastest turnaround of SLC-40 to date at 9 days. Previous record: SLC-40 at 29 days",
                    "– Fastest turnaround of SpaceX to date at 9 days. Previous record: 29 days",
                    "– 5th Falcon 9 mission",
                    "– 3rd Falcon 9 flight with a flight-proven booster",
                    "– 5th reflight of a Falcon booster",
                    "– 5th reflight of a Falcon booster in 2024",
                    "– 6th SpaceX launch of 2024",
                    "– 6th SpaceX launch from SLC-40",
                ],
            },
        )
