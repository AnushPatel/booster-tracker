from django.test import TestCase
from unittest.mock import patch
from .test_helpers import initialize_test_data, update_data
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
    SpacecraftOnLaunch,
)
from booster_tracker.utils import TurnaroundObjects
from datetime import datetime
import pytz


class TestRocketModel(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_num_launches(self):
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


class TestStageModel(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_num_launches(self):
        self.assertEqual(self.test_data["b1062"].num_launches, 3)
        self.assertEqual(self.test_data["b1080"].num_launches, 3)
        self.assertEqual(self.test_data["b1084"].num_launches, 1)
        self.assertEqual(self.test_data["b1085"].num_launches, 0)

    def test_fastest_turnaround(self):
        self.assertEqual(self.test_data["b1062"].fastest_turnaround, 2678400)
        self.assertEqual(self.test_data["b1080"].fastest_turnaround, 2592000)
        # test stage with only a single launch
        self.assertIsNone(self.test_data["b1084"].fastest_turnaround)
        # test stage with zero launches
        self.assertIsNone(self.test_data["b1085"].fastest_turnaround)


class TestSpacecraftModel(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_num_launches(self):
        self.assertEqual(self.test_data["c206"].num_launches, 2)
        self.assertEqual(self.test_data["c207"].num_launches, 0)

    def test_fastest_turnaround(self):
        self.assertEqual(self.test_data["c206"].fastest_turnaround, 1468800)
        self.assertIsNone(self.test_data["c207"].fastest_turnaround)


class TestPadModel(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_num_launches(self):
        self.assertEqual(self.test_data["slc40"].num_launches, 5)
        self.assertEqual(self.test_data["lc39a"].num_launches, 0)
        self.assertEqual(self.test_data["slc4e"].num_launches, 0)

    def test_fastest_turnaround(self):
        self.assertEqual(self.test_data["slc40"].fastest_turnaround, 2505600)
        self.assertIsNone(self.test_data["lc39a"].fastest_turnaround)
        self.assertIsNone(self.test_data["slc4e"].fastest_turnaround)


class TestLaunchModel(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_droneship_needed(self):
        # Test perm launch objects
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").droneship_needed, False)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").droneship_needed, False)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").droneship_needed, True)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").droneship_needed, True)

    def test_flight_proven_booster(self):
        # Test perm stage and recoveries
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").flight_proven_stage, False)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").flight_proven_stage, True)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").flight_proven_stage, True)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").flight_proven_stage, True)

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
            Launch.objects.get(name="Falcon Heavy Temp Launch 1").flight_proven_stage,
            False,
        )

    def test_get_company_turnaround(self):
        self.assertIsNone(self.test_data["launch1"].get_company_turnaround)
        self.assertEqual(self.test_data["launch2"].get_company_turnaround, 2678400)
        self.assertEqual(self.test_data["launch3"].get_company_turnaround, 2505600)
        self.assertEqual(self.test_data["launch4"].get_company_turnaround, 2678400)

    def test_get_pad_turnaround(self):
        self.assertIsNone(self.test_data["launch1"].get_pad_turnaround)
        self.assertEqual(self.test_data["launch2"].get_pad_turnaround, 2678400)
        self.assertEqual(self.test_data["launch3"].get_pad_turnaround, 2505600)
        self.assertEqual(self.test_data["launch4"].get_pad_turnaround, 2678400)

    def test_get_stage_flights_and_turnaround(self):
        # Test on perm StageAndRecovery objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").get_stage_flights(
                stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 1"))
            ),
            1,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").get_stage_flights(
                stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 2"))
            ),
            2,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_stage_flights(
                stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 3"))
            ),
            1,
        )

        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights(stage=Stage.objects.get(name="B1062")),
            3,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights(stage=Stage.objects.get(name="B1080")),
            2,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights(stage=Stage.objects.get(name="B1084")),
            1,
        )

    def test_calculate_stage_and_recovery_turnaround_stats(self):
        # Ensure stats correct for perm launches
        stage_stats = self.test_data["launch1"].calculate_stage_and_recovery_turnaround_stats("booster")
        zone_stats = self.test_data["launch1"].calculate_stage_and_recovery_turnaround_stats("landing_zone")
        self.assertEqual(stage_stats, [])
        self.assertEqual(zone_stats, [])

        stage_stats = self.test_data["launch2"].calculate_stage_and_recovery_turnaround_stats("booster")
        zone_stats = self.test_data["launch2"].calculate_stage_and_recovery_turnaround_stats("landing_zone")
        self.assertEqual(stage_stats, [])
        self.assertEqual(zone_stats, [])

        stage_stats = self.test_data["launch3"].calculate_stage_and_recovery_turnaround_stats("booster")
        zone_stats = self.test_data["launch3"].calculate_stage_and_recovery_turnaround_stats("landing_zone")
        self.assertEqual(stage_stats, [])
        self.assertEqual(zone_stats, [])

        stage_stats = self.test_data["launch4"].calculate_stage_and_recovery_turnaround_stats("booster")
        zone_stats = self.test_data["launch4"].calculate_stage_and_recovery_turnaround_stats("landing_zone")
        self.assertEqual(stage_stats, [])
        self.assertEqual(zone_stats, [])

        stage_stats = self.test_data["launch5"].calculate_stage_and_recovery_turnaround_stats("booster")
        zone_stats = self.test_data["launch5"].calculate_stage_and_recovery_turnaround_stats("landing_zone")
        self.assertEqual(
            stage_stats,
            [(True, "Fastest turnaround of a Falcon booster to date at 30 days. Previous record: B1062 at 31 days")],
        )
        self.assertEqual(zone_stats, [])

        # Add launches with zone and booster records

        temp_launch_1 = Launch.objects.create(
            time=datetime(2024, 5, 15, tzinfo=pytz.utc),
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
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        update_data()

        stage_stats = temp_launch_1.calculate_stage_and_recovery_turnaround_stats("booster")
        zone_stats = temp_launch_1.calculate_stage_and_recovery_turnaround_stats("landing_zone")
        self.assertEqual(
            stage_stats,
            [(True, "Fastest turnaround of a Falcon booster to date at 14 days. Previous record: B1080 at 30 days")],
        )
        self.assertEqual(
            zone_stats,
            [
                (
                    True,
                    "Fastest turnaround of a Falcon recovery zone to date at 14 days. Previous record: Landing Zone 1 at 29 days",
                )
            ],
        )

    def test_calculate_turnaround_stats(self):
        pad_stats = self.test_data["launch1"].calculate_pad_turnaround_stats()
        company_stats = self.test_data["launch1"].calculate_company_turnaround_stats()
        self.assertEqual(pad_stats, [])
        self.assertEqual(company_stats, [])

        pad_stats = self.test_data["launch2"].calculate_pad_turnaround_stats()
        company_stats = self.test_data["launch2"].calculate_company_turnaround_stats()
        self.assertEqual(pad_stats, [])
        self.assertEqual(company_stats, [])

        pad_stats = self.test_data["launch3"].calculate_pad_turnaround_stats()
        company_stats = self.test_data["launch3"].calculate_company_turnaround_stats()
        self.assertEqual(
            pad_stats,
            [(True, "Fastest turnaround of a SpaceX pad to date at 29 days. Previous record: SLC-40 at 31 days")],
        )
        self.assertEqual(
            company_stats,
            [(True, "Shortest time between two SpaceX launches to date at 29 days. Previous record: 31 days")],
        )

        pad_stats = self.test_data["launch4"].calculate_pad_turnaround_stats()
        company_stats = self.test_data["launch4"].calculate_company_turnaround_stats()
        self.assertEqual(pad_stats, [])
        self.assertEqual(company_stats, [])

        pad_stats = self.test_data["launch5"].calculate_pad_turnaround_stats()
        company_stats = self.test_data["launch5"].calculate_company_turnaround_stats()
        self.assertEqual(pad_stats, [])
        self.assertEqual(company_stats, [])

        temp_launch_1 = Launch.objects.create(
            time=datetime(2024, 5, 15, tzinfo=pytz.utc),
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
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        update_data()

        pad_stats = temp_launch_1.calculate_pad_turnaround_stats()
        company_stats = temp_launch_1.calculate_company_turnaround_stats()
        self.assertEqual(
            pad_stats,
            [(True, "Fastest turnaround of a SpaceX pad to date at 14 days. Previous record: SLC-40 at 29 days")],
        )
        self.assertEqual(
            company_stats,
            [(True, "Shortest time between two SpaceX launches to date at 14 days. Previous record: 29 days")],
        )

        # Ensure pad-specific stats work:
        Launch.objects.create(
            time=datetime(2024, 5, 16, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 6, 15, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        temp_launch_4 = Launch.objects.create(
            time=datetime(2024, 7, 10, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 4",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass=1000,
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        update_data()

        pad_stats = temp_launch_4.calculate_pad_turnaround_stats()
        company_stats = temp_launch_4.calculate_company_turnaround_stats()
        self.assertEqual(
            pad_stats, [(True, "Fastest turnaround of LC-39A to date at 25 days. Previous record: 30 days")]
        )

    def test_boosters(self):
        # Test for perm objects
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").stages, "B1062-1")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").stages, "B1062-2")
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").stages,
            "B1084-1, B1080-2, and B1062-3",
        )
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").stages, "B1080-3")

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
        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").stages, "Unknown")

    def test_make_booster_display(self):
        # Test for perm objects; space is intentional for formatting in table
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").make_stage_display(),
            " B1062-1; N/A-day turnaround",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").make_stage_display(),
            " B1062-2; 31.00-day turnaround",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").make_stage_display(),
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
            Launch.objects.get(name="Falcon 9 Temp Launch 1").make_stage_display(),
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
            "B1080 successfully completed a landing on Just Read the Instructions (JRtI)",
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
            Launch.objects.get(name="Falcon 9 Launch 1").make_stats(return_significant_only=False),
            [
                (False, "1st Falcon 9 launch"),
                (False, "1st Falcon 9 launch in 2024"),
                (False, "1st Falcon 9 launch success"),
                (False, "1st SpaceX launch from SLC-40"),
                (False, "1st SpaceX mission"),
                (False, "1st SpaceX mission success"),
                (False, "1st SpaceX launch"),
                (False, "1st SpaceX launch of 2024"),
                (False, "1st Falcon booster landing success on a ground pad"),
                (False, "1st landing attempt of a Falcon booster"),
            ],
        )

        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").make_stats(return_significant_only=False),
            [
                (False, "2nd Falcon 9 launch"),
                (False, "2nd Falcon 9 launch in 2024"),
                (False, "2nd Falcon 9 launch success"),
                (False, "1st Falcon 9 launch with a flight-proven stage"),
                (False, "2nd SpaceX launch from SLC-40"),
                (False, "2nd SpaceX mission"),
                (False, "2nd SpaceX mission success"),
                (False, "2nd SpaceX launch"),
                (False, "2nd SpaceX launch of 2024"),
                (False, "2nd Falcon booster landing success on a ground pad"),
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").make_stats(return_significant_only=False),
            [
                (False, "3rd Falcon 9 launch"),
                (False, "3rd Falcon 9 launch in 2024"),
                (False, "3rd Falcon 9 launch success"),
                (False, "3rd SpaceX launch from SLC-40"),
                (False, "3rd SpaceX mission"),
                (False, "3rd SpaceX mission success"),
                (False, "3rd SpaceX launch"),
                (False, "3rd SpaceX launch of 2024"),
                (False, "3rd Falcon booster landing success on a ground pad"),
                (False, "3rd landing attempt of a Falcon booster"),
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").make_stats(return_significant_only=False),
            [
                (False, "1st Falcon Heavy launch"),
                (False, "1st Falcon Heavy launch in 2024"),
                (False, "1st Falcon Heavy launch success"),
                (False, "1st Falcon Heavy launch with a flight-proven stage"),
                (False, "4th SpaceX launch from SLC-40"),
                (False, "4th SpaceX mission"),
                (False, "4th SpaceX mission success"),
                (False, "4th SpaceX launch"),
                (False, "4th SpaceX launch of 2024"),
                (False, "4th Falcon booster landing success on a ground pad"),
            ],
        )

        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").make_stats(return_significant_only=True),
            [],
        )

        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").make_stats(return_significant_only=False),
            [
                (False, "4th Falcon 9 launch"),
                (False, "4th Falcon 9 launch in 2024"),
                (False, "4th Falcon 9 launch success"),
                (False, "2nd Falcon 9 launch with a flight-proven stage"),
                (False, "5th SpaceX launch from SLC-40"),
                (False, "5th SpaceX mission"),
                (False, "5th SpaceX mission success"),
                (False, "5th SpaceX launch"),
                (False, "5th SpaceX launch of 2024"),
                (False, "2nd Falcon booster landing success on a drone ship"),
            ],
        )

    @patch("random.randint")
    def test_create_x_post(self, mock_randint):
        mock_randint.side_effect = [0, 1]
        launch = Launch.objects.get(name="Falcon 9 Launch 1")
        result = launch.make_x_post()

        expected = f"{launch.name} will mark SpaceX's 1st Falcon 9 launch success and 1st Falcon 9 launch.\n\nLearn more: https://boostertracker.com/launch/{launch.id}"

        self.assertEqual(result, expected)
        self.assertTrue(len(result) <= 280)

        # Test with a different random selection
        mock_randint.side_effect = [1, 0]
        launch = Launch.objects.get(name="Falcon 9 Launch 3")
        result = launch.make_x_post()

        expected = f"{launch.name} will mark SpaceX's fastest turnaround of a pad to date at 29 days and shortest time between two launches to date at 29 days.\n\nLearn more: https://boostertracker.com/launch/{launch.id}"

        self.assertEqual(result, expected)
        self.assertTrue(len(result) <= 280)

        launch = Launch.objects.get(name="Falcon 9 Launch 4")
        mock_randint.side_effect = [0, 0]
        result = launch.make_x_post()

        expected = f"{launch.name} will mark SpaceX's 4th Falcon 9 launch and fastest turnaround of a Falcon booster to date at 30 days.\n\nLearn more: https://boostertracker.com/launch/{launch.id}"

        self.assertEqual(result, expected)
        self.assertTrue(len(result) <= 280)

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
                    "– 1st Falcon 9 launch",
                    "– 1st Falcon 9 launch in 2024",
                    "– 1st Falcon 9 launch success",
                    "– 1st SpaceX launch from SLC-40",
                    "– 1st SpaceX mission",
                    "– 1st SpaceX mission success",
                    "– 1st SpaceX launch",
                    "– 1st SpaceX launch of 2024",
                    "– 1st Falcon booster landing success on a ground pad",
                    "– 1st landing attempt of a Falcon booster",
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
                    "– 2nd Falcon 9 launch",
                    "– 2nd Falcon 9 launch in 2024",
                    "– 2nd Falcon 9 launch success",
                    "– 1st Falcon 9 launch with a flight-proven stage",
                    "– 2nd SpaceX launch from SLC-40",
                    "– 2nd SpaceX mission",
                    "– 2nd SpaceX mission success",
                    "– 2nd SpaceX launch",
                    "– 2nd SpaceX launch of 2024",
                    "– 2nd Falcon booster landing success on a ground pad",
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
                    "– 3rd Falcon 9 launch",
                    "– 3rd Falcon 9 launch in 2024",
                    "– 3rd Falcon 9 launch success",
                    "– 3rd SpaceX launch from SLC-40",
                    "– 3rd SpaceX mission",
                    "– 3rd SpaceX mission success",
                    "– 3rd SpaceX launch",
                    "– 3rd SpaceX launch of 2024",
                    "– 3rd Falcon booster landing success on a ground pad",
                    "– 3rd landing attempt of a Falcon booster",
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
                    "– 1st Falcon Heavy launch",
                    "– 1st Falcon Heavy launch in 2024",
                    "– 1st Falcon Heavy launch success",
                    "– 1st Falcon Heavy launch with a flight-proven stage",
                    "– 4th SpaceX launch from SLC-40",
                    "– 4th SpaceX mission",
                    "– 4th SpaceX mission success",
                    "– 4th SpaceX launch",
                    "– 4th SpaceX launch of 2024",
                    "– 4th Falcon booster landing success on a ground pad",
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
                "Where did the first stage land?": [
                    "B1080 successfully completed a landing on Just Read the Instructions (JRtI)",
                    "",
                    "Tug: N/A; Support: N/A",
                ],
                "Did they attempt to recover the fairings?": ["There are no fairings on this flight"],
                "This was the": [
                    "– 4th Falcon 9 launch",
                    "– 4th Falcon 9 launch in 2024",
                    "– 4th Falcon 9 launch success",
                    "– 2nd Falcon 9 launch with a flight-proven stage",
                    "– 5th SpaceX launch from SLC-40",
                    "– 5th SpaceX mission",
                    "– 5th SpaceX mission success",
                    "– 5th SpaceX launch",
                    "– 5th SpaceX launch of 2024",
                    "– 2nd Falcon booster landing success on a drone ship",
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

    def test_get_rocket_stats(self):
        self.assertEqual(
            self.test_data["launch1"].get_rocket_stats(),
            [
                (False, "1st Falcon 9 launch"),
                (False, "1st Falcon 9 launch in 2024"),
                (False, "1st Falcon 9 launch success"),
            ],
        )

        self.assertEqual(
            self.test_data["launch2"].get_rocket_stats(),
            [
                (False, "2nd Falcon 9 launch"),
                (False, "2nd Falcon 9 launch in 2024"),
                (False, "2nd Falcon 9 launch success"),
                (False, "1st Falcon 9 launch with a flight-proven stage"),
            ],
        )

        self.assertEqual(
            self.test_data["launch3"].get_rocket_stats(),
            [
                (False, "3rd Falcon 9 launch"),
                (False, "3rd Falcon 9 launch in 2024"),
                (False, "3rd Falcon 9 launch success"),
            ],
        )

        self.assertEqual(
            self.test_data["launch4"].get_rocket_stats(),
            [
                (False, "1st Falcon Heavy launch"),
                (False, "1st Falcon Heavy launch in 2024"),
                (False, "1st Falcon Heavy launch success"),
                (False, "1st Falcon Heavy launch with a flight-proven stage"),
            ],
        )

        self.assertEqual(
            self.test_data["launch5"].get_rocket_stats(),
            [
                (False, "4th Falcon 9 launch"),
                (False, "4th Falcon 9 launch in 2024"),
                (False, "4th Falcon 9 launch success"),
                (False, "2nd Falcon 9 launch with a flight-proven stage"),
            ],
        )

    def test_get_launch_provider_stats(self):
        self.assertEqual(
            self.test_data["launch1"].get_launch_provider_stats(),
            [
                (False, "1st SpaceX mission"),
                (False, "1st SpaceX mission success"),
                (False, "1st SpaceX launch"),
                (False, "1st SpaceX launch of 2024"),
            ],
        )

        self.assertEqual(
            self.test_data["launch2"].get_launch_provider_stats(),
            [
                (False, "2nd SpaceX mission"),
                (False, "2nd SpaceX mission success"),
                (False, "2nd SpaceX launch"),
                (False, "2nd SpaceX launch of 2024"),
            ],
        )

        self.assertEqual(
            self.test_data["launch3"].get_launch_provider_stats(),
            [
                (False, "3rd SpaceX mission"),
                (False, "3rd SpaceX mission success"),
                (False, "3rd SpaceX launch"),
                (False, "3rd SpaceX launch of 2024"),
            ],
        )

        self.assertEqual(
            self.test_data["launch4"].get_launch_provider_stats(),
            [
                (False, "4th SpaceX mission"),
                (False, "4th SpaceX mission success"),
                (False, "4th SpaceX launch"),
                (False, "4th SpaceX launch of 2024"),
            ],
        )

        self.assertEqual(
            self.test_data["launch5"].get_launch_provider_stats(),
            [
                (False, "5th SpaceX mission"),
                (False, "5th SpaceX mission success"),
                (False, "5th SpaceX launch"),
                (False, "5th SpaceX launch of 2024"),
            ],
        )

    def test_get_launch_pad_stats(self):
        self.assertEqual(self.test_data["launch1"].get_launch_pad_stats(), [(False, "1st SpaceX launch from SLC-40")])
        self.assertEqual(self.test_data["launch2"].get_launch_pad_stats(), [(False, "2nd SpaceX launch from SLC-40")])
        self.assertEqual(self.test_data["launch3"].get_launch_pad_stats(), [(False, "3rd SpaceX launch from SLC-40")])
        self.assertEqual(self.test_data["launch4"].get_launch_pad_stats(), [(False, "4th SpaceX launch from SLC-40")])
        self.assertEqual(self.test_data["launch5"].get_launch_pad_stats(), [(False, "5th SpaceX launch from SLC-40")])


class TestLandingZoneModel(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_num_landings(self):
        self.assertEqual(self.test_data["lz1"].num_landings, 4)
        self.assertEqual(self.test_data["lz2"].num_landings, 1)
        self.assertEqual(self.test_data["jrti"].num_landings, 2)

    def test_fastest_turnaround(self):
        self.assertEqual(self.test_data["lz1"].fastest_turnaround, 2505600)
        self.assertIsNone(self.test_data["lz2"].fastest_turnaround)
        self.assertEqual(self.test_data["jrti"].fastest_turnaround, 2592000)


class TestStageAndRecoveryModel(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_get_num_flights(self):
        self.assertEqual(self.test_data["launch1_sr"].get_num_flights, 1)
        self.assertEqual(self.test_data["launch2_sr"].get_num_flights, 2)
        self.assertEqual(self.test_data["launch3_sr"].get_num_flights, 1)
        self.assertEqual(self.test_data["launch4_sr1"].get_num_flights, 2)
        self.assertEqual(self.test_data["launch4_sr2"].get_num_flights, 3)
        self.assertEqual(self.test_data["launch4_sr3"].get_num_flights, 1)
        self.assertEqual(self.test_data["launch5_sr"].get_num_flights, 3)

    def test_get_num_landings(self):
        self.assertEqual(self.test_data["launch1_sr"].get_num_landings, 1)
        self.assertEqual(self.test_data["launch2_sr"].get_num_landings, 2)
        self.assertEqual(self.test_data["launch3_sr"].get_num_landings, 3)
        self.assertEqual(self.test_data["launch4_sr1"].get_num_landings, 4)
        self.assertEqual(self.test_data["launch4_sr2"].get_num_landings, 1)
        self.assertEqual(self.test_data["launch4_sr3"].get_num_landings, 1)
        self.assertEqual(self.test_data["launch5_sr"].get_num_landings, 2)

    def test_get_stage_turnaround(self):
        self.assertIsNone(self.test_data["launch1_sr"].get_stage_turnaround)
        self.assertEqual(self.test_data["launch2_sr"].get_stage_turnaround, 2678400)
        self.assertIsNone(self.test_data["launch3_sr"].get_stage_turnaround)
        self.assertEqual(self.test_data["launch4_sr1"].get_stage_turnaround, 2678400)
        self.assertEqual(self.test_data["launch4_sr2"].get_stage_turnaround, 5184000)
        self.assertIsNone(self.test_data["launch4_sr3"].get_stage_turnaround)
        self.assertEqual(self.test_data["launch5_sr"].get_stage_turnaround, 2592000)

    def test_get_zone_turnaround(self):
        self.assertIsNone(self.test_data["launch1_sr"].get_zone_turnaround)
        self.assertEqual(self.test_data["launch2_sr"].get_zone_turnaround, 2678400)
        self.assertEqual(self.test_data["launch3_sr"].get_zone_turnaround, 2505600)
        self.assertEqual(self.test_data["launch4_sr1"].get_zone_turnaround, 2678400)
        self.assertIsNone(self.test_data["launch4_sr2"].get_zone_turnaround)
        self.assertIsNone(self.test_data["launch4_sr3"].get_zone_turnaround)
        self.assertEqual(self.test_data["launch5_sr"].get_zone_turnaround, 2592000)

    def test_get_stage_stats(self):
        expected = [
            (False, "1st Falcon booster landing success on a ground pad"),
            (False, "1st landing attempt of a Falcon booster"),
            (False, "1st landing success of a Falcon booster"),
            (False, "1st consecutive landing of a Falcon booster"),
        ]
        self.assertEqual(StageAndRecovery.objects.get(launch=self.test_data["launch1"]).get_stage_stats(), expected)

        expected = [
            (False, "2nd Falcon booster landing success on a ground pad"),
            (False, "2nd landing attempt of a Falcon booster"),
            (False, "2nd landing success of a Falcon booster"),
            (False, "2nd consecutive landing of a Falcon booster"),
            (False, "1st reflight of a Falcon booster"),
            (False, "1st reflight of a Falcon booster in 2024"),
        ]
        self.assertEqual(StageAndRecovery.objects.get(launch=self.test_data["launch2"]).get_stage_stats(), expected)

        expected = [
            (False, "3rd Falcon booster landing success on a ground pad"),
            (False, "3rd landing attempt of a Falcon booster"),
            (False, "3rd landing success of a Falcon booster"),
            (False, "3rd consecutive landing of a Falcon booster"),
        ]
        self.assertEqual(StageAndRecovery.objects.get(launch=self.test_data["launch3"]).get_stage_stats(), expected)

        expected = [
            (False, "4th Falcon booster landing success on a ground pad"),
            (False, "4th landing attempt of a Falcon booster"),
            (False, "4th landing success of a Falcon booster"),
            (False, "4th consecutive landing of a Falcon booster"),
            (False, "2nd reflight of a Falcon booster"),
            (False, "2nd reflight of a Falcon booster in 2024"),
        ]
        self.assertEqual(
            StageAndRecovery.objects.filter(launch=self.test_data["launch4"]).order_by("id").first().get_stage_stats(),
            expected,
        )

        expected = [
            (False, "5th Falcon booster landing success on a ground pad"),
            (False, "5th landing attempt of a Falcon booster"),
            (False, "5th landing success of a Falcon booster"),
            (False, "5th consecutive landing of a Falcon booster"),
            (False, "3rd reflight of a Falcon booster"),
            (False, "3rd reflight of a Falcon booster in 2024"),
        ]
        self.assertEqual(
            StageAndRecovery.objects.filter(launch=self.test_data["launch4"]).order_by("id")[1].get_stage_stats(),
            expected,
        )

        expected = [
            (False, "1st Falcon booster landing success on a drone ship"),
            (False, "6th landing attempt of a Falcon booster"),
            (False, "6th landing success of a Falcon booster"),
            (False, "6th consecutive landing of a Falcon booster"),
        ]
        self.assertEqual(
            StageAndRecovery.objects.filter(launch=self.test_data["launch4"]).order_by("id")[2].get_stage_stats(),
            expected,
        )

        expected = [
            (False, "2nd Falcon booster landing success on a drone ship"),
            (False, "7th landing attempt of a Falcon booster"),
            (False, "7th landing success of a Falcon booster"),
            (False, "7th consecutive landing of a Falcon booster"),
            (False, "4th reflight of a Falcon booster"),
            (False, "4th reflight of a Falcon booster in 2024"),
        ]
        self.assertEqual(StageAndRecovery.objects.get(launch=self.test_data["launch5"]).get_stage_stats(), expected)

    def test_get_landing_zone_stats(self):
        expected = [(False, "1st landing success on Landing Zone 1"), (False, "1st landing attempt on Landing Zone 1")]
        self.assertEqual(
            StageAndRecovery.objects.get(launch=self.test_data["launch1"]).get_landing_zone_stats(), expected
        )

        expected = [(False, "2nd landing success on Landing Zone 1"), (False, "2nd landing attempt on Landing Zone 1")]
        self.assertEqual(
            StageAndRecovery.objects.get(launch=self.test_data["launch2"]).get_landing_zone_stats(), expected
        )

        expected = [(False, "3rd landing success on Landing Zone 1"), (False, "3rd landing attempt on Landing Zone 1")]
        self.assertEqual(
            StageAndRecovery.objects.get(launch=self.test_data["launch3"]).get_landing_zone_stats(), expected
        )

        expected = [(False, "4th landing success on Landing Zone 1"), (False, "4th landing attempt on Landing Zone 1")]
        self.assertEqual(
            StageAndRecovery.objects.filter(launch=self.test_data["launch4"])
            .order_by("id")
            .first()
            .get_landing_zone_stats(),
            expected,
        )

        expected = [(False, "1st landing success on Landing Zone 2"), (False, "1st landing attempt on Landing Zone 2")]
        self.assertEqual(
            StageAndRecovery.objects.filter(launch=self.test_data["launch4"])
            .order_by("id")[1]
            .get_landing_zone_stats(),
            expected,
        )

        expected = [
            (False, "1st landing success on Just Read the Instructions"),
            (False, "1st landing attempt on Just Read the Instructions"),
        ]
        self.assertEqual(
            StageAndRecovery.objects.filter(launch=self.test_data["launch4"])
            .order_by("id")[2]
            .get_landing_zone_stats(),
            expected,
        )

        expected = [
            (False, "2nd landing success on Just Read the Instructions"),
            (False, "2nd landing attempt on Just Read the Instructions"),
        ]
        self.assertEqual(
            StageAndRecovery.objects.get(launch=self.test_data["launch5"]).get_landing_zone_stats(), expected
        )


class TestSpacecraftOnLaunchModel(TestCase):
    def setUp(self):
        self.test_data = initialize_test_data()

    def test_get_num_flights(self):
        self.assertEqual(SpacecraftOnLaunch.objects.get(launch=self.test_data["launch1"]).get_num_flights(), 1)
        self.assertEqual(SpacecraftOnLaunch.objects.get(launch=self.test_data["launch2"]).get_num_flights(), 2)

    def test_get_turnaround(self):
        self.assertIsNone(SpacecraftOnLaunch.objects.get(launch=self.test_data["launch1"]).get_turnaround())
        self.assertEqual(SpacecraftOnLaunch.objects.get(launch=self.test_data["launch2"]).get_turnaround(), 1468800)

    def test_get_spacecraft_stats(self):
        self.assertEqual(
            SpacecraftOnLaunch.objects.get(launch=self.test_data["launch1"]).get_spacecraft_stats(),
            [
                (False, "1st launch of Dragon"),
                (False, "1st launch of Dragon None"),
                (False, "1st launch of Cargo Dragon"),
            ],
        )
        self.assertEqual(
            SpacecraftOnLaunch.objects.get(launch=self.test_data["launch2"]).get_spacecraft_stats(),
            [
                (False, "2nd launch of Dragon"),
                (False, "2nd launch of Dragon None"),
                (False, "2nd launch of Cargo Dragon"),
                (False, "1st reuse of a Dragon spacecraft"),
            ],
        )
