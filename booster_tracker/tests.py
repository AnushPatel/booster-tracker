from django.test import TestCase
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
)
from booster_tracker.utils import (
    format_time,
    convert_seconds,
    make_ordinal,
    concatenated_list,
    TurnaroundObjects,
    turnaround_time,
)
from booster_tracker.home_utils import (
    get_landings_and_successes,
    get_most_flown_boosters,
)
from datetime import datetime
import pytz


class TestCases(TestCase):
    def setUp(self):
        # Set up database with objects that will be perm throughout all tests
        Operator.objects.create(name="SpaceX")
        Rocket.objects.create(
            name="Falcon 9", provider=Operator.objects.get(name="SpaceX")
        )
        Rocket.objects.create(
            name="Falcon Heavy", provider=Operator.objects.get(name="SpaceX")
        )

        Pad.objects.create(
            name="Space Launch Complex 40",
            nickname="SLC-40",
            location="CCSFS",
            status="ACTIVE",
        )
        Pad.objects.create(
            name="Launch Complex 39A",
            nickname="LC-39A",
            location="KSC",
            status="ACTIVE",
        )
        Orbit.objects.create(name="low-Earth Orbit")

        Boat.objects.create(name="Doug", type="SUPPORT")
        Boat.objects.create(name="Bob", type="SUPPORT")

        LandingZone.objects.create(
            name="Landing Zone 1", nickname="LZ-1", status="ACTIVE"
        )
        LandingZone.objects.create(
            name="Landing Zone 2", nickname="LZ-2", status="ACTIVE"
        )
        LandingZone.objects.create(
            name="Just Read the Instructions", nickname="JRtI", status="ACTIVE"
        )

        Stage.objects.create(
            name="B1062",
            rocket=Rocket.objects.get(name="Falcon 9"),
            version="v1.2 Block 5.4",
            type="BOOSTER",
            status="ACTIVE",
        )
        Stage.objects.create(
            name="B1080",
            rocket=Rocket.objects.get(name="Falcon 9"),
            version="v1.2 Block 5.5",
            type="BOOSTER",
            status="ACTIVE",
        )
        Stage.objects.create(
            name="B1084",
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            version="v1.2 Block 5.5",
            type="BOOSTER",
            status="ACTIVE",
        )

        PadUsed.objects.create(
            rocket=Rocket.objects.get(name="Falcon 9"),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
        )
        PadUsed.objects.create(
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            pad=Pad.objects.get(name="Launch Complex 39A"),
        )
        PadUsed.objects.create(
            rocket=Rocket.objects.get(name="Falcon 9"),
            pad=Pad.objects.get(name="Launch Complex 39A"),
        )

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 2, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 3, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Launch 4",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Launch 1"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Launch 2"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Launch 3"),
            stage=Stage.objects.get(name="B1080"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
            stage=Stage.objects.get(name="B1080"),
            stage_position="MY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
            stage=Stage.objects.get(name="B1062"),
            stage_position="PY",
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
            stage=Stage.objects.get(name="B1084"),
            stage_position="CENTER",
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Launch 4"),
            stage=Stage.objects.get(name="B1080"),
            method="EXPENDED",
            method_success="SUCCESS",
            recovery_success=False,
        )

    # Start by testing all of the functions in the # utils.py folder
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
        self.assertEqual(
            convert_seconds(90061), "1 day, 1 hour, 1 minute, and 1 second"
        )
        self.assertEqual(
            convert_seconds(195330), "2 days, 6 hours, 15 minutes, and 30 seconds"
        )
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
        self.assertEqual(
            concatenated_list(["Bob", "Doug", "GO Beyond"]), "Bob, Doug, and GO Beyond"
        )
        self.assertEqual(concatenated_list(["Bob", "Doug"]), "Bob and Doug")
        self.assertEqual(concatenated_list(["Bob"]), "Bob")
        self.assertEqual(concatenated_list([]), "N/A")

    def test_get_most_flown_boosters(self):
        # Ensure most flown boosters being grabbed successfully
        self.assertEqual(get_most_flown_boosters(), (["B1062", "B1080"], 3))

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
        self.assertEqual(get_most_flown_boosters(), (["B1080"], 4))

    def test_turnaround_time(self):
        self.assertIsNone(turnaround_time([]))
        self.assertEqual(
            turnaround_time(Launch.objects.all().order_by("time")), 2592000
        )

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
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="FAILURE",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="FAILURE",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        # Test function on additional launches
        self.assertEqual(Rocket.objects.get(name="Falcon 9").num_successes, 4)
        self.assertEqual(Rocket.objects.get(name="Falcon Heavy").num_successes, 2)

    def test_get_landings_and_successes(self):
        # Test function on perm objects
        self.assertEqual(get_landings_and_successes(), (6, 6))

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
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
            method_success="FAILURE",
            recovery_success=False,
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage=Stage.objects.get(name="B1084"),
            stage_position="CENTER",
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="FAILURE",
            recovery_success=False,
        )

        # following the addition of three landing attempts (two successful), ensure function responds accordingly
        self.assertEqual(get_landings_and_successes(), (9, 7))

    # Test the methods for pads and landing zones
    def test_num_launches(self):
        # Test number of launches and landings on perm objects
        self.assertEqual(Pad.objects.get(nickname="SLC-40").num_launches, 5)
        self.assertEqual(Pad.objects.get(nickname="LC-39A").num_launches, 0)

        self.assertEqual(LandingZone.objects.get(nickname="LZ-1").num_landings, 4)
        self.assertEqual(LandingZone.objects.get(nickname="LZ-2").num_landings, 1)
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").num_landings, 1)

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
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
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").num_landings, 1)

        Launch.objects.create(
            time=datetime(2024, 4, 2, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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
        self.assertEqual(LandingZone.objects.get(nickname="JRtI").num_landings, 1)

    def test_fastest_turnaround(self):
        # Test with perm objects
        self.assertEqual(
            Pad.objects.get(nickname="SLC-40").fastest_turnaround, "29 days"
        )
        self.assertEqual(Pad.objects.get(nickname="LC-39A").fastest_turnaround, "N/A")

        self.assertEqual(
            LandingZone.objects.get(nickname="LZ-1").fastest_turnaround, "29 days"
        )
        self.assertEqual(
            LandingZone.objects.get(nickname="LZ-2").fastest_turnaround, "N/A"
        )
        self.assertEqual(
            LandingZone.objects.get(nickname="JRtI").fastest_turnaround, "N/A"
        )

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
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
            landing_zone=LandingZone.objects.get(name="Landing Zone 2"),
            method="GROUND_PAD",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Ensure after adding launch that is not new quickest does not update stats
        self.assertEqual(
            Pad.objects.get(nickname="SLC-40").fastest_turnaround, "29 days"
        )
        self.assertEqual(Pad.objects.get(nickname="LC-39A").fastest_turnaround, "N/A")

        self.assertEqual(
            LandingZone.objects.get(nickname="LZ-1").fastest_turnaround, "29 days"
        )
        self.assertEqual(
            LandingZone.objects.get(nickname="LZ-2").fastest_turnaround, "N/A"
        )
        self.assertEqual(
            LandingZone.objects.get(nickname="JRtI").fastest_turnaround, "N/A"
        )

        Launch.objects.create(
            time=datetime(2024, 4, 2, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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

        # Ensure stats update correctly with new quickest turnaround
        self.assertEqual(
            Pad.objects.get(nickname="SLC-40").fastest_turnaround, "29 days"
        )
        self.assertEqual(Pad.objects.get(nickname="LC-39A").fastest_turnaround, "1 day")

        self.assertEqual(
            LandingZone.objects.get(nickname="LZ-1").fastest_turnaround, "1 day"
        )
        self.assertEqual(
            LandingZone.objects.get(nickname="LZ-2").fastest_turnaround, "N/A"
        )
        self.assertEqual(
            LandingZone.objects.get(nickname="JRtI").fastest_turnaround, "N/A"
        )

    # And now test functions in models.py
    def test_droneship_needed(self):
        # Test perm launch objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").droneship_needed, False
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").droneship_needed, False
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").droneship_needed, True
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").droneship_needed, False
        )

    def test_flight_proven_booster(self):
        # Test perm stage and recoveries
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").flight_proven_booster, False
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").flight_proven_booster, True
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").flight_proven_booster, True
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").flight_proven_booster, True
        )

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
            mass="1000 kg",
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
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").num_successful_landings, 1
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").num_successful_landings, 1
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").num_successful_landings, 3
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").num_successful_landings, 0
        )

    def test_get_stage_flights_and_turnaround(self):
        # Test on perm StageAndRecovery objects
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Launch 1"
            ).get_stage_flights_and_turnaround(
                stage=Stage.objects.get(
                    stageandrecovery__launch=Launch.objects.get(
                        name="Falcon 9 Launch 1"
                    )
                )
            ),
            (1, None),
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Launch 2"
            ).get_stage_flights_and_turnaround(
                stage=Stage.objects.get(
                    stageandrecovery__launch=Launch.objects.get(
                        name="Falcon 9 Launch 2"
                    )
                )
            ),
            (2, 31.00),
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Launch 3"
            ).get_stage_flights_and_turnaround(
                stage=Stage.objects.get(
                    stageandrecovery__launch=Launch.objects.get(
                        name="Falcon 9 Launch 3"
                    )
                )
            ),
            (1, None),
        )

        self.assertEqual(
            Launch.objects.get(
                name="Falcon Heavy Launch 1"
            ).get_stage_flights_and_turnaround(stage=Stage.objects.get(name="B1062")),
            (3, 60.00),
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon Heavy Launch 1"
            ).get_stage_flights_and_turnaround(stage=Stage.objects.get(name="B1080")),
            (2, 31.00),
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon Heavy Launch 1"
            ).get_stage_flights_and_turnaround(stage=Stage.objects.get(name="B1084")),
            (1, None),
        )

    def test_get_rocket_flights_reused_vehicle(self):
        # Test on perm objects
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Launch 1"
            ).get_rocket_flights_reused_vehicle(),
            0,
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Launch 2"
            ).get_rocket_flights_reused_vehicle(),
            1,
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Launch 3"
            ).get_rocket_flights_reused_vehicle(),
            1,
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon Heavy Launch 1"
            ).get_rocket_flights_reused_vehicle(),
            1,
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Launch 4"
            ).get_rocket_flights_reused_vehicle(),
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
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 7, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 8, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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

        # Ensure function updates as expected for Falcon launches with varying number of flight proven boosters
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Temp Launch 1"
            ).get_rocket_flights_reused_vehicle(),
            2,
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Temp Launch 2"
            ).get_rocket_flights_reused_vehicle(),
            3,
        )
        self.assertEqual(
            Launch.objects.get(
                name="Falcon Heavy Temp Launch 1"
            ).get_rocket_flights_reused_vehicle(),
            2,
        )

    def test_get_total_reflights(self):
        # Just some random date that is before all launches
        past_time = datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc)
        # A time that is between launches to ensure offset works
        later_time = datetime(2024, 2, 2, 0, 0, tzinfo=pytz.utc)
        # Test perm launch objects for all time
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").get_total_reflights(
                start=past_time
            ),
            "N/A",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").get_total_reflights(
                start=past_time
            ),
            "1st",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_total_reflights(
                start=past_time
            ),
            "N/A",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_total_reflights(
                start=past_time
            ),
            "2nd and 3rd",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").get_total_reflights(
                start=past_time
            ),
            "4th",
        )

        # later_time is after first launch but before all launches after; ensure that the numbers above drop by one
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_total_reflights(
                start=later_time
            ),
            "N/A",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_total_reflights(
                start=later_time
            ),
            "1st and 2nd",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").get_total_reflights(
                start=later_time
            ),
            "3rd",
        )

    def test_get_num_booster_landings(self):
        # Test on perm launch objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").get_num_booster_landings(),
            "1st",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").get_num_booster_landings(),
            "2nd",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_num_booster_landings(),
            "3rd",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_num_booster_landings(),
            "4th, 5th, and 6th",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").get_num_booster_landings(),
            None,
        )

        Launch.objects.create(
            time=datetime(2024, 6, 1, 0, 0, tzinfo=pytz.utc),
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

        # Ensure function responds accordingly
        self.assertEqual(
            Launch.objects.get(
                name="Falcon 9 Temp Launch 1"
            ).get_num_booster_landings(),
            "7th",
        )

    def test_calculate_turnarounds(self):
        # Test perm launch objects
        # Start by testing the ALL case
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.ALL
            ),
            None,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.ALL
            ),
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
            Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.ALL
            ),
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
            Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(
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
            Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.PAD
            ),
            None,
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.PAD
            ),
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
            Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(
                turnaround_object=TurnaroundObjects.PAD
            ),
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
            Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(
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

        Launch.objects.create(
            time=datetime(2024, 4, 2, 0, 0, tzinfo=pytz.utc),
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
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

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
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").get_consec_landings(), "1st"
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").get_consec_landings(), "2nd"
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").get_consec_landings(), "3rd"
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").get_consec_landings(),
            "4th, 5th, and 6th",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").get_consec_landings(), "N/A"
        )

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
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
            method="GROUND_PAD",
            method_success="FAILURE",
            recovery_success=True,
        )

        # Ensure a landing failure resets count
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").get_consec_landings(),
            "N/A",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 3, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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
            Launch.objects.get(name="Falcon 9 Temp Launch 2").get_consec_landings(),
            "1st",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 4, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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
            Launch.objects.get(name="Falcon Heavy Temp Launch 1").get_consec_landings(),
            "1st and 2nd",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 5, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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
            Launch.objects.get(name="Falcon Heavy Temp Launch 2").get_consec_landings(),
            "1st",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 6, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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
            Launch.objects.get(name="Falcon Heavy Temp Launch 3").get_consec_landings(),
            "N/A",
        )

        today = datetime.now(pytz.utc)
        Launch.objects.create(
            time=datetime(today.year, today.month + 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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
            Launch.objects.get(name="Falcon 9 Temp Launch 3").get_consec_landings(),
            "1st",
        )

    def test_get_boosters(self):
        # Test for perm objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").boosters, "B1062-1"
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").boosters, "B1062-2"
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").boosters,
            "B1084-1, B1080-2, and B1062-3",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").boosters, "B1080-3"
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

        # Ensure launch with no booster assigned gets unknown
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").boosters, "Unknown"
        )

    def test_get_recoveries(self):
        # Test for perm objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").recoveries, "LZ-1"
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").recoveries, "LZ-1"
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").recoveries,
            "JRtI, LZ-1, and LZ-2",
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").recoveries, "Expended"
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

        # Test for when no recovery information added
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").recoveries, "N/A"
        )

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
            mass="1000 kg",
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
            "B1080 successfully completed a landing on Landing Zone 1 (LZ-1); B1062 successfully completed a landing on Landing Zone 2 (LZ-2); B1084 successfully completed a landing on Just Read the Instructions (JRtI)",
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
            mass="1000 kg",
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
            mass="1000 kg",
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
            mass="1000 kg",
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
            mass="1000 kg",
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
                "– 1st Falcon 9 mission",
                "– 1st booster landing",
                "– 1st consecutive booster landing",
                "– 1st SpaceX launch of 2024",
                "– 1st SpaceX launch from Space Launch Complex 40",
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").make_stats(),
            [
                "– 2nd Falcon 9 mission",
                "– 1st Falcon 9 flight with a flight-proven booster",
                "– 1st reflight of a booster",
                "– 1st reflight of a booster in 2024",
                "– 2nd booster landing",
                "– 2nd consecutive booster landing",
                "– 2nd SpaceX launch of 2024",
                "– 2nd SpaceX launch from Space Launch Complex 40",
                "– Qickest turnaround of a booster to date at 31 days",
                "– Quickest turnaround time of a landing zone to date at 31 days",
                "– Shortest time between any two SpaceX launches at 31 days",
                "– Qickest turnaround of a SpaceX pad to date at 31 days",
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").make_stats(),
            [
                "– 3rd Falcon 9 mission",
                "– 3rd booster landing",
                "– 3rd consecutive booster landing",
                "– 3rd SpaceX launch of 2024",
                "– 3rd SpaceX launch from Space Launch Complex 40",
                "– Quickest turnaround time of a landing zone to date at 29 days. Previous record: LZ-1 at 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
                "– Shortest time between any two SpaceX launches at 29 days. Previous record: 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
                "– Qickest turnaround of a SpaceX pad to date at 29 days. Previous record: SLC-40 at 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").make_stats(),
            [
                "– 1st Falcon Heavy mission",
                "– 1st Falcon Heavy flight with a flight-proven booster",
                "– 2nd and 3rd reflight of a booster",
                "– 2nd and 3rd reflight of a booster in 2024",
                "– 4th, 5th, and 6th booster landings",
                "– 4th, 5th, and 6th consecutive booster landings",
                "– 4th SpaceX launch of 2024",
                "– 4th SpaceX launch from Space Launch Complex 40",
                "– Quickest turnaround of B1080 to date at 31 days",
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").make_stats(),
            [
                "– 4th Falcon 9 mission",
                "– 2nd Falcon 9 flight with a flight-proven booster",
                "– 4th reflight of a booster",
                "– 4th reflight of a booster in 2024",
                "– 5th SpaceX launch of 2024",
                "– 5th SpaceX launch from Space Launch Complex 40",
                "– Qickest turnaround of a booster to date at 30 days. Previous record: B1062 at 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
            ],
        )

        Launch.objects.create(
            time=datetime(2024, 5, 1, 0, 1, tzinfo=pytz.utc),
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
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Just Read the Instructions"),
            method="DRONE_SHIP",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Test stats update for additional launch
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").make_stats(),
            [
                "– 5th Falcon 9 mission",
                "– 3rd Falcon 9 flight with a flight-proven booster",
                "– 5th reflight of a booster",
                "– 5th reflight of a booster in 2024",
                "– 7th booster landing",
                "– 7th consecutive booster landing",
                "– 6th SpaceX launch of 2024",
                "– 6th SpaceX launch from Space Launch Complex 40",
                "– Quickest turnaround of B1062 to date at 30 days and 1 minute. Previous record: 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
                "– Qickest turnaround of JRtI to date at 30 days and 1 minute",
                "– Shortest time between any two SpaceX launches at 1 minute. Previous record: 29 days between Falcon 9 Launch 2 and Falcon 9 Launch 3",
                "– Qickest turnaround of a SpaceX pad to date at 1 minute. Previous record: SLC-40 at 29 days between Falcon 9 Launch 2 and Falcon 9 Launch 3",
            ],
        )

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome="SUCCESS",
        )

        Launch.objects.create(
            time=datetime(2024, 5, 12, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Launch Complex 39A"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
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

        # Test to ensure quickest turnaround stats work
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 2").make_stats(),
            [
                "– 6th Falcon 9 mission",
                "– 4th Falcon 9 flight with a flight-proven booster",
                "– 6th reflight of a booster",
                "– 6th reflight of a booster in 2024",
                "– 8th booster landing",
                "– 8th consecutive booster landing",
                "– 7th SpaceX launch of 2024",
                "– 1st SpaceX launch from Launch Complex 39A",
                "– Qickest turnaround of a booster to date at 23 hours and 59 minutes. Previous record: B1080 at 30 days between Falcon Heavy Launch 1 and Falcon 9 Launch 4",
                "– Quickest turnaround time of a landing zone to date at 23 hours and 59 minutes. Previous record: LZ-1 at 29 days between Falcon 9 Launch 2 and Falcon 9 Launch 3",
            ],
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 3").make_stats(),
            [
                "– 7th Falcon 9 mission",
                "– 5th Falcon 9 flight with a flight-proven booster",
                "– 7th reflight of a booster",
                "– 7th reflight of a booster in 2024",
                "– 9th booster landing",
                "– 9th consecutive booster landing",
                "– 8th SpaceX launch of 2024",
                "– 2nd SpaceX launch from Launch Complex 39A",
                "– Qickest turnaround of LC-39A to date at 10 days",
            ],
        )

    def test_create_launch_table(self):
        # Test for perm objects
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 1").create_launch_table(),
            {
                "Lift Off Time": [
                    "January 01, 2024 - 00:00 UTC",
                    "December 31, 2023 - 19:00 EST",
                ],
                "Mission Name": ["Falcon 9 Launch 1"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1062-1; N/A-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1000 kg"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": [
                    "B1062 successfully completed a landing on Landing Zone 1 (LZ-1)"
                ],
                "Did they attempt to recover the fairings?": [
                    "There are no fairings on this flight"
                ],
                "This was the": [
                    "– 1st Falcon 9 mission",
                    "– 1st booster landing",
                    "– 1st consecutive booster landing",
                    "– 1st SpaceX launch of 2024",
                    "– 1st SpaceX launch from Space Launch Complex 40",
                ],
                "Where to watch": ["Official coverage"],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 2").create_launch_table(),
            {
                "Lift Off Time": [
                    "February 01, 2024 - 00:00 UTC",
                    "January 31, 2024 - 19:00 EST",
                ],
                "Mission Name": ["Falcon 9 Launch 2"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1062-2; 31.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1000 kg"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": [
                    "B1062 successfully completed a landing on Landing Zone 1 (LZ-1)"
                ],
                "Did they attempt to recover the fairings?": [
                    "There are no fairings on this flight"
                ],
                "This was the": [
                    "– 2nd Falcon 9 mission",
                    "– 1st Falcon 9 flight with a flight-proven booster",
                    "– 1st reflight of a booster",
                    "– 1st reflight of a booster in 2024",
                    "– 2nd booster landing",
                    "– 2nd consecutive booster landing",
                    "– 2nd SpaceX launch of 2024",
                    "– 2nd SpaceX launch from Space Launch Complex 40",
                    "– Qickest turnaround of a booster to date at 31 days",
                    "– Quickest turnaround time of a landing zone to date at 31 days",
                    "– Shortest time between any two SpaceX launches at 31 days",
                    "– Qickest turnaround of a SpaceX pad to date at 31 days",
                ],
                "Where to watch": ["Official coverage"],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 3").create_launch_table(),
            {
                "Lift Off Time": [
                    "March 01, 2024 - 00:00 UTC",
                    "February 29, 2024 - 19:00 EST",
                ],
                "Mission Name": ["Falcon 9 Launch 3"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1080-1; N/A-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1000 kg"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": [
                    "B1080 successfully completed a landing on Landing Zone 1 (LZ-1)"
                ],
                "Did they attempt to recover the fairings?": [
                    "There are no fairings on this flight"
                ],
                "This was the": [
                    "– 3rd Falcon 9 mission",
                    "– 3rd booster landing",
                    "– 3rd consecutive booster landing",
                    "– 3rd SpaceX launch of 2024",
                    "– 3rd SpaceX launch from Space Launch Complex 40",
                    "– Quickest turnaround time of a landing zone to date at 29 days. Previous record: LZ-1 at 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
                    "– Shortest time between any two SpaceX launches at 29 days. Previous record: 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
                    "– Qickest turnaround of a SpaceX pad to date at 29 days. Previous record: SLC-40 at 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
                ],
                "Where to watch": ["Official coverage"],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon Heavy Launch 1").create_launch_table(),
            {
                "Lift Off Time": [
                    "April 01, 2024 - 00:00 UTC",
                    "March 31, 2024 - 20:00 EDT",
                ],
                "Mission Name": ["Falcon Heavy Launch 1"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": [
                    "Falcon Heavy B1084-1, B1080-2, B1062-3; N/A, 31.00, 60.00-day turnaround"
                ],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1000 kg"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": [
                    "B1080 successfully completed a landing on Landing Zone 1 (LZ-1); B1062 successfully completed a landing on Landing Zone 2 (LZ-2); B1084 successfully completed a landing on Just Read the Instructions (JRtI)",
                    "",
                    "Tug: N/A; Support: N/A",
                ],
                "Did they attempt to recover the fairings?": [
                    "There are no fairings on this flight"
                ],
                "This was the": [
                    "– 1st Falcon Heavy mission",
                    "– 1st Falcon Heavy flight with a flight-proven booster",
                    "– 2nd and 3rd reflight of a booster",
                    "– 2nd and 3rd reflight of a booster in 2024",
                    "– 4th, 5th, and 6th booster landings",
                    "– 4th, 5th, and 6th consecutive booster landings",
                    "– 4th SpaceX launch of 2024",
                    "– 4th SpaceX launch from Space Launch Complex 40",
                    "– Quickest turnaround of B1080 to date at 31 days",
                ],
                "Where to watch": ["Official coverage"],
            },
        )
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Launch 4").create_launch_table(),
            {
                "Lift Off Time": [
                    "May 01, 2024 - 00:00 UTC",
                    "April 30, 2024 - 20:00 EDT",
                ],
                "Mission Name": ["Falcon 9 Launch 4"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1080-3; 30.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1000 kg"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": ["B1080 was expended"],
                "Did they attempt to recover the fairings?": [
                    "There are no fairings on this flight"
                ],
                "This was the": [
                    "– 4th Falcon 9 mission",
                    "– 2nd Falcon 9 flight with a flight-proven booster",
                    "– 4th reflight of a booster",
                    "– 4th reflight of a booster in 2024",
                    "– 5th SpaceX launch of 2024",
                    "– 5th SpaceX launch from Space Launch Complex 40",
                    "– Qickest turnaround of a booster to date at 30 days. Previous record: B1062 at 31 days between Falcon 9 Launch 1 and Falcon 9 Launch 2",
                ],
                "Where to watch": ["Official coverage"],
            },
        )

        Launch.objects.create(
            time=datetime(datetime.now(pytz.utc).year + 1, 5, 1, 0, 0, tzinfo=pytz.utc),
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
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="OCEAN_SURFACE",
            method_success="SUCCESS",
            recovery_success=True,
        )

        # Test for additional launch that is landing on ocean surface
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 1").create_launch_table(),
            {
                "Lift Off Time": [
                    "May 01, 2025 - 00:00 UTC",
                    "April 30, 2025 - 20:00 EDT",
                ],
                "Mission Name": ["Falcon 9 Temp Launch 1"],
                "Launch Provider <br /> (What rocket company is launching it?)": [
                    "SpaceX"
                ],
                "Customer <br /> (Who's paying for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1062-4; 395.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1000 kg"],
                "Where are the satellites going?": ["low-Earth Orbit"],
                "Where will the first stage land?": [
                    "B1062 will attempt a soft landing on the ocean surface"
                ],
                "Will they be attempting to recover the fairings?": [
                    "There are no fairings on this flight"
                ],
                "How's the weather looking?": [
                    "The weather is currently XX% go for launch"
                ],
                "This will be the": [
                    "– 5th Falcon 9 mission",
                    "– 3rd Falcon 9 flight with a flight-proven booster",
                    "– 5th reflight of a booster",
                    "– 1st reflight of a booster in 2025",
                    "– 1st SpaceX launch of 2025",
                    "– 6th SpaceX launch from Space Launch Complex 40",
                ],
                "Where to watch": ["Official coverage"],
            },
        )

        Launch.objects.create(
            time=datetime(2024, 5, 10, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
        )

        StageAndRecovery.objects.create(
            launch=Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage=Stage.objects.get(name="B1062"),
            landing_zone=LandingZone.objects.get(name="Landing Zone 1"),
            method="DRONE_SHIP",
            recovery_success=True,
        )

        # Test additional launch for drone ship
        self.assertEqual(
            Launch.objects.get(name="Falcon 9 Temp Launch 2").create_launch_table(),
            {
                "Lift Off Time": [
                    "May 10, 2024 - 00:00 UTC",
                    "May 09, 2024 - 20:00 EDT",
                ],
                "Mission Name": ["Falcon 9 Temp Launch 2"],
                "Launch Provider <br /> (What rocket company launched it?)": ["SpaceX"],
                "Customer <br /> (Who paid for this?)": ["SpaceX"],
                "Rocket": ["Falcon 9 B1062-4; 39.00-day turnaround"],
                "Launch Location": ["Space Launch Complex 40 (SLC-40), CCSFS"],
                "Payload mass": ["1000 kg"],
                "Where did the satellites go?": ["low-Earth Orbit"],
                "Where did the first stage land?": [
                    "B1062 successfully completed a landing on Landing Zone 1 (LZ-1)",
                    "",
                    "Tug: N/A; Support: N/A",
                ],
                "Did they attempt to recover the fairings?": [
                    "There are no fairings on this flight"
                ],
                "This was the": [
                    "– 5th Falcon 9 mission",
                    "– 3rd Falcon 9 flight with a flight-proven booster",
                    "– 5th reflight of a booster",
                    "– 5th reflight of a booster in 2024",
                    "– 6th SpaceX launch of 2024",
                    "– 6th SpaceX launch from Space Launch Complex 40",
                    "– Shortest time between any two SpaceX launches at 9 days. Previous record: 29 days between Falcon 9 Launch 2 and Falcon 9 Launch 3",
                    "– Qickest turnaround of a SpaceX pad to date at 9 days. Previous record: SLC-40 at 29 days between Falcon 9 Launch 2 and Falcon 9 Launch 3",
                ],
                "Where to watch": ["Official coverage"],
            },
        )
