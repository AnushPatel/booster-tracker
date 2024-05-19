from django.test import TestCase
from booster_tracker.models import *
from booster_tracker.utils import *

# Create your tests here.
class StatsTestCases(TestCase):
    def setUp(self):
        Operator.objects.create(name="SpaceX")
        Rocket.objects.create(name="Falcon 9", provider=Operator.objects.get(name="SpaceX"))
        Rocket.objects.create(name="Falcon Heavy", provider=Operator.objects.get(name="SpaceX"))

        Pad.objects.create(name="Space Launch Complex 40", nickname="SLC-40", location="CCSFS", status="ACTIVE")
        Orbit.objects.create(name="low-Earth Orbit")

        Boat.objects.create(name="Doug", type="SUPPORT")
        Boat.objects.create(name="Bob", type="SUPPORT")

        LandingZone.objects.create(name="Landing Zone 1", nickname="LZ-1", status="ACTIVE")
        LandingZone.objects.create(name="Landing Zone 2", nickname="LZ-2", status="ACTIVE")
        LandingZone.objects.create(name="Just Read the Instructions", nickname="JRtI", status="ACTIVE")

        Stage.objects.create(name="B1062", rocket=Rocket.objects.get(name="Falcon 9"), version="v1.2 Block 5.4", type="BOOSTER", status="ACTIVE")
        Stage.objects.create(name="B1080", rocket=Rocket.objects.get(name="Falcon 9"), version="v1.2 Block 5.5", type="BOOSTER", status="ACTIVE")
        Stage.objects.create(name="B1084", rocket=Rocket.objects.get(name="Falcon Heavy"), version="v1.2 Block 5.5", type="BOOSTER", status="ACTIVE")

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        Launch.objects.create(
            time=datetime(2024, 2, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        Launch.objects.create(
            time=datetime(2024, 3, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        Launch.objects.create(
            time=datetime(2024, 5, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Launch 4",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Launch 1"),
            stage = Stage.objects.get(name="B1062"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Launch 2"),
            stage = Stage.objects.get(name="B1062"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Launch 3"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Launch 1"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Launch 1"),
            stage = Stage.objects.get(name="B1062"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 2"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Launch 1"),
            stage = Stage.objects.get(name="B1084"),
            landing_zone = LandingZone.objects.get(name="Just Read the Instructions"),
            method = "DRONE_SHIP",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Launch 4"),
            stage = Stage.objects.get(name="B1080"),
            method = "EXPENDED",
            method_success = "SUCCESS",
            recovery_success = False
        )

    #Start by testing all of the functions in the #utils.py folder
    def test_format_time(self):
        self.assertEqual(format_time(datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc)), "January 01, 2024 - 00:00 UTC")
        self.assertEqual(format_time(datetime(2024, 3, 14, 14, 32, tzinfo=pytz.utc)), "March 14, 2024 - 14:32 UTC")
    
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

    def test_get_most_flown_boosters(self):
        self.assertEqual(get_most_flown_boosters(), (["B1062", "B1080"], 3))

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "DRONE_SHIP",
            method_success = "SUCCESS",
            recovery_success = True
        )

        self.assertEqual(get_most_flown_boosters(), (["B1080"], 4))

    def test_remove_duplicates(self):
        self.assertCountEqual(remove_duplicates([Boat.objects.get(name="Bob"), Boat.objects.get(name="Doug")]), ["Bob", "Doug"])
        self.assertEqual(remove_duplicates([Boat.objects.get(name="Bob"), Boat.objects.get(name="Bob")]), ["Bob"])

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
            launch_outcome = "SUCCESS"
        )

        self.assertEqual(turnaround_time(Launch.objects.all().order_by("time")), 86400)

    #And now test functions in models.py
    def test_droneship_needed(self):
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").droneship_needed, False)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").droneship_needed, False)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").droneship_needed, True)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").droneship_needed, False)

    def test_flight_proven_booster(self):
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").flight_proven_booster, False)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").flight_proven_booster, True)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").flight_proven_booster, True)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").flight_proven_booster, True)

        Stage.objects.create(name="B1000", rocket=Rocket.objects.get(name="Falcon 9"), version="v1.2 Block 5.4", type="BOOSTER", status="ACTIVE")
        Stage.objects.create(name="B1001", rocket=Rocket.objects.get(name="Falcon 9"), version="v1.2 Block 5.5", type="BOOSTER", status="ACTIVE")
        Stage.objects.create(name="B1002", rocket=Rocket.objects.get(name="Falcon Heavy"), version="v1.2 Block 5.5", type="BOOSTER", status="ACTIVE")

        Launch.objects.create(
            time=datetime(2024, 4, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1000"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1001"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 2"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1002"),
            landing_zone = LandingZone.objects.get(name="Just Read the Instructions"),
            method = "DRONE_SHIP",
            method_success = "SUCCESS",
            recovery_success = True
        )

        self.assertEqual(Launch.objects.get(name="Falcon Heavy Temp Launch 1").flight_proven_booster, False)

    def test_num_successful_landings(self):
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").num_successful_landings, 1)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").num_successful_landings, 1)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").num_successful_landings, 3)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").num_successful_landings, 0)

    def test_get_stage_flights_and_turnaround(self):
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").get_stage_flights_and_turnaround(stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 1"))), (1, None))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").get_stage_flights_and_turnaround(stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 2"))), (2, 31.00))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").get_stage_flights_and_turnaround(stage=Stage.objects.get(stageandrecovery__launch=Launch.objects.get(name="Falcon 9 Launch 3"))), (1, None))

        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights_and_turnaround(stage=Stage.objects.get(name="B1062")), (3, 60.00))
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights_and_turnaround(stage=Stage.objects.get(name="B1080")), (2, 31.00))
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_stage_flights_and_turnaround(stage=Stage.objects.get(name="B1084")), (1, None))

    def test_get_rocket_flights_reused_vehicle(self):

        Stage.objects.create(name="B1081", rocket=Rocket.objects.get(name="Falcon 9"), version="v1.2 Block 5.5", type="BOOSTER", status="ACTIVE")

        Launch.objects.create(
            time=datetime(2024, 6, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        Launch.objects.create(
            time=datetime(2024, 7, 1, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        Launch.objects.create(
            time=datetime(2024, 8, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage = Stage.objects.get(name="B1081"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage = Stage.objects.get(name="B1081"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1062"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 2"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1084"),
            landing_zone = LandingZone.objects.get(name="Just Read the Instructions"),
            method = "DRONE_SHIP",
            method_success = "SUCCESS",
            recovery_success = True
        )

        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").get_rocket_flights_reused_vehicle(), 0)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").get_rocket_flights_reused_vehicle(), 1)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").get_rocket_flights_reused_vehicle(), 1)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").get_rocket_flights_reused_vehicle(), 2)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").get_rocket_flights_reused_vehicle(), 2)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 2").get_rocket_flights_reused_vehicle(), 3)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_rocket_flights_reused_vehicle(), 1)
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Temp Launch 1").get_rocket_flights_reused_vehicle(), 2)

    def test_get_total_reflights(self):
        past_time = datetime(2000, 1, 1, 0, 0, tzinfo=pytz.utc) #Just some random date that is before all launches
        later_time = datetime(2024, 2, 2, 0, 0, tzinfo=pytz.utc) #A time that is between launches to ensure offset works
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").get_total_reflights(start=past_time), "N/A")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").get_total_reflights(start=past_time), "1st")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").get_total_reflights(start=past_time), "N/A")
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_total_reflights(start=past_time), "2nd and 3rd")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").get_total_reflights(start=past_time), "4th")

        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").get_total_reflights(start=later_time), "N/A")
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_total_reflights(start=later_time), "1st and 2nd")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").get_total_reflights(start=later_time), "3rd")

    def test_get_num_booster_landings(self):
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").get_num_booster_landings(), "1st")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").get_num_booster_landings(), "2nd")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").get_num_booster_landings(), "3rd")
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_num_booster_landings(), "4th, 5th, and 6th")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").get_num_booster_landings(), None)

        Launch.objects.create(
            time=datetime(2024, 6, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "DRONE_SHIP",
            method_success = "SUCCESS",
            recovery_success = True
        )

        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").get_num_booster_landings(), "7th")

    def test_calculate_turnarounds(self):
        #Start by testing the ALL case
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(object=TurnaroundObjects.ALL), None)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(object=TurnaroundObjects.ALL), (True, [['', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(object=TurnaroundObjects.ALL), (True, [['', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1']]))
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").calculate_turnarounds(object=TurnaroundObjects.ALL), (False, [['', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(object=TurnaroundObjects.ALL), (False, [['', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['', 2592000, 'Falcon 9 Launch 4', 'Falcon Heavy Launch 1'], ['', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))

        #Testing of BOOSTER case
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(object=TurnaroundObjects.BOOSTER), None)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(object=TurnaroundObjects.BOOSTER), (True, [['B1062', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(object=TurnaroundObjects.BOOSTER), (False, [['B1062', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1']]))
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").calculate_turnarounds(object=TurnaroundObjects.BOOSTER), (False, [['B1062', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['B1080', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3'], ['B1062', 5184000, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 2']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(object=TurnaroundObjects.BOOSTER), (True, [['B1080', 2592000, 'Falcon 9 Launch 4', 'Falcon Heavy Launch 1'], ['B1062', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['B1080', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3'], ['B1062', 5184000, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 2']]))

        #Testing of PAD case
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(object=TurnaroundObjects.PAD), None)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(object=TurnaroundObjects.PAD), (True, [['SLC-40', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(object=TurnaroundObjects.PAD), (True, [['SLC-40', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['SLC-40', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1']]))
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").calculate_turnarounds(object=TurnaroundObjects.PAD), (False, [['SLC-40', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['SLC-40', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['SLC-40', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(object=TurnaroundObjects.PAD), (False, [['SLC-40', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['SLC-40', 2592000, 'Falcon 9 Launch 4', 'Falcon Heavy Launch 1'], ['SLC-40', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['SLC-40', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))

        #Testing of LANDING_ZONE case
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").calculate_turnarounds(object=TurnaroundObjects.LANDING_ZONE), None)
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").calculate_turnarounds(object=TurnaroundObjects.LANDING_ZONE), (True, [['LZ-1', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").calculate_turnarounds(object=TurnaroundObjects.LANDING_ZONE), (True, [['LZ-1', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['LZ-1', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1']]))
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").calculate_turnarounds(object=TurnaroundObjects.LANDING_ZONE), (False, [['LZ-1', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['LZ-1', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['LZ-1', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").calculate_turnarounds(object=TurnaroundObjects.LANDING_ZONE), (False, [['LZ-1', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['LZ-1', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['LZ-1', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))

        #Make sure it responds correctly when another launch is added
        Launch.objects.create(
            time=datetime(2024, 4, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Just Read the Instructions"),
            method = "DRONE_SHIP",
            method_success = "SUCCESS",
            recovery_success = True
        )

        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").calculate_turnarounds(object=TurnaroundObjects.BOOSTER), (True, [['B1080', 86400, 'Falcon 9 Temp Launch 1', 'Falcon Heavy Launch 1'], ['B1062', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['B1080', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3'], ['B1062', 5184000, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 2']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").calculate_turnarounds(object=TurnaroundObjects.PAD), (True, [['SLC-40', 86400, 'Falcon 9 Temp Launch 1', 'Falcon Heavy Launch 1'], ['SLC-40', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['SLC-40', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['SLC-40', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").calculate_turnarounds(object=TurnaroundObjects.LANDING_ZONE), (True, [['JRtI', 86400, 'Falcon 9 Temp Launch 1', 'Falcon Heavy Launch 1'], ['LZ-1', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['LZ-1', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['LZ-1', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))
        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").calculate_turnarounds(object=TurnaroundObjects.ALL), (True, [['', 86400, 'Falcon 9 Temp Launch 1', 'Falcon Heavy Launch 1'], ['', 2505600, 'Falcon 9 Launch 3', 'Falcon 9 Launch 2'], ['', 2678400, 'Falcon 9 Launch 2', 'Falcon 9 Launch 1'], ['', 2678400, 'Falcon Heavy Launch 1', 'Falcon 9 Launch 3']]))

    def test_get_consec_landings(self):
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").get_consec_landings(), "1st")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").get_consec_landings(), "2nd")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 3").get_consec_landings(), "3rd")
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_consec_landings(), "4th, 5th, and 6th")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").get_consec_landings(), "N/A")

        Launch.objects.create(
            time=datetime(2024, 5, 2, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Temp Launch 1"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "FAILURE",
            recovery_success = True
        )

        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").get_consec_landings(), "N/A")

        Launch.objects.create(
            time=datetime(2024, 5, 3, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 2",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Temp Launch 2"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 2").get_consec_landings(), "1st")

        Launch.objects.create(
            time=datetime(2024, 5, 4, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon Heavy"),
            name="Falcon Heavy Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1062"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            method_success = "FAILURE",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1080"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 2"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon Heavy Temp Launch 1"),
            stage = Stage.objects.get(name="B1084"),
            landing_zone = LandingZone.objects.get(name="Just Read the Instructions"),
            method = "GROUND_PAD",
            method_success = "SUCCESS",
            recovery_success = True
        )

        self.assertEqual(Launch.objects.get(name="Falcon Heavy Temp Launch 1").get_consec_landings(), "1st and 2nd")

        today = datetime.now(pytz.utc)
        Launch.objects.create(
            time=datetime(today.year, today.month + 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 3",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        StageAndRecovery.objects.create(
            launch = Launch.objects.get(name="Falcon 9 Temp Launch 3"),
            stage = Stage.objects.get(name="B1062"),
            landing_zone = LandingZone.objects.get(name="Landing Zone 1"),
            method = "GROUND_PAD",
            recovery_success = False
        )

        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 3").get_consec_landings(), "3rd")

    def test_get_boosters(self):
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").get_boosters(), "B1062-1")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").get_boosters(), "B1062-2")
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_boosters(), "B1080-2, B1062-3, and B1084-1")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").get_boosters(), "B1080-3")

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").get_boosters(), "N/A")

    def test_get_recoveries(self):
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 1").get_recoveries(), "LZ-1")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 2").get_recoveries(), "LZ-1")
        self.assertEqual(Launch.objects.get(name="Falcon Heavy Launch 1").get_recoveries(), "LZ-1, LZ-2, and JRtI")
        self.assertEqual(Launch.objects.get(name="Falcon 9 Launch 4").get_recoveries(), "Expended")

        Launch.objects.create(
            time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
            pad=Pad.objects.get(name="Space Launch Complex 40"),
            rocket=Rocket.objects.get(name="Falcon 9"),
            name="Falcon 9 Temp Launch 1",
            orbit=Orbit.objects.get(name="low-Earth Orbit"),
            mass="1000 kg",
            customer="SpaceX",
            launch_outcome = "SUCCESS"
        )

        self.assertEqual(Launch.objects.get(name="Falcon 9 Temp Launch 1").get_recoveries(), "N/A")