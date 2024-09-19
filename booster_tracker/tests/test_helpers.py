from datetime import datetime, timedelta
import pytz
from booster_tracker.models import (
    Operator,
    RocketFamily,
    Rocket,
    Pad,
    Orbit,
    Boat,
    LandingZone,
    Stage,
    PadUsed,
    Launch,
    StageAndRecovery,
    SpacecraftFamily,
    SpacecraftOnLaunch,
    Spacecraft,
)


def initialize_test_data():
    # Create operators
    spacex = Operator.objects.create(name="SpaceX")

    # Create rocket families and rockets
    falcon_family = RocketFamily.objects.create(name="Falcon", provider=spacex)
    falcon_9 = Rocket.objects.create(name="Falcon 9", family=falcon_family)
    falcon_heavy = Rocket.objects.create(name="Falcon Heavy", family=falcon_family)

    # Create spacecraft data
    dragon = SpacecraftFamily.objects.create(name="Dragon", provider=spacex)
    c206 = Spacecraft.objects.create(name="C206", type="CARGO", family=dragon)
    c207 = Spacecraft.objects.create(name="C207", type="CARGO", family=dragon)

    # Create pads
    slc40 = Pad.objects.create(
        name="Space Launch Complex 40",
        nickname="SLC-40",
        location="CCSFS",
        status="ACTIVE",
    )
    lc39a = Pad.objects.create(
        name="Launch Complex 39A",
        nickname="LC-39A",
        location="KSC",
        status="ACTIVE",
    )

    slc4e = Pad.objects.create(name="Space Launch Complex 4 East", nickname="SLC-4E", location="Vandy", status="ACTIVE")

    # Create orbit
    low_earth_orbit = Orbit.objects.create(name="low-Earth Orbit")

    # Create boats
    Boat.objects.create(name="Doug", type="SUPPORT")
    Boat.objects.create(name="Bob", type="SUPPORT")

    # Create landing zones
    lz1 = LandingZone.objects.create(name="Landing Zone 1", nickname="LZ-1", status="ACTIVE")
    lz2 = LandingZone.objects.create(name="Landing Zone 2", nickname="LZ-2", status="ACTIVE")
    jrti = LandingZone.objects.create(name="Just Read the Instructions", nickname="JRtI", status="ACTIVE")

    # Create stages
    b1062 = Stage.objects.create(
        name="B1062",
        rocket=falcon_9,
        version="v1.2 Block 5.4",
        type="BOOSTER",
        status="ACTIVE",
    )
    b1080 = Stage.objects.create(
        name="B1080",
        rocket=falcon_9,
        version="v1.2 Block 5.5",
        type="BOOSTER",
        status="ACTIVE",
    )
    b1084 = Stage.objects.create(
        name="B1084",
        rocket=falcon_heavy,
        version="v1.2 Block 5.5",
        type="BOOSTER",
        status="ACTIVE",
    )
    b1085 = Stage.objects.create(
        name="B1085",
        rocket=falcon_heavy,
        version="v1.2 Block 5.5",
        type="BOOSTER",
        status="ACTIVE",
    )

    # Create pad usage
    PadUsed.objects.create(
        rocket=falcon_9,
        pad=slc40,
    )
    PadUsed.objects.create(
        rocket=falcon_heavy,
        pad=slc40,
    )
    PadUsed.objects.create(
        rocket=falcon_9,
        pad=lc39a,
    )

    # Create launches
    launch1 = Launch.objects.create(
        time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
        pad=slc40,
        rocket=falcon_9,
        name="Falcon 9 Launch 1",
        orbit=low_earth_orbit,
        mass=1000,
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )
    launch2 = Launch.objects.create(
        time=datetime(2024, 2, 1, tzinfo=pytz.utc),
        pad=slc40,
        rocket=falcon_9,
        name="Falcon 9 Launch 2",
        orbit=low_earth_orbit,
        mass=1000,
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )
    launch3 = Launch.objects.create(
        time=datetime(2024, 3, 1, tzinfo=pytz.utc),
        pad=slc40,
        rocket=falcon_9,
        name="Falcon 9 Launch 3",
        orbit=low_earth_orbit,
        mass=1000,
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )
    launch4 = Launch.objects.create(
        time=datetime(2024, 4, 1, tzinfo=pytz.utc),
        pad=slc40,
        rocket=falcon_heavy,
        name="Falcon Heavy Launch 1",
        orbit=low_earth_orbit,
        mass=1000,
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )
    launch5 = Launch.objects.create(
        time=datetime(2024, 5, 1, 0, 0, tzinfo=pytz.utc),
        pad=slc40,
        rocket=falcon_9,
        name="Falcon 9 Launch 4",
        orbit=low_earth_orbit,
        mass=1000,
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )

    # Create stage and recovery
    launch1_sr = StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon 9 Launch 1"),
        stage=b1062,
        landing_zone=lz1,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    launch2_sr = StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon 9 Launch 2"),
        stage=b1062,
        landing_zone=lz1,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    launch3_sr = StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon 9 Launch 3"),
        stage=b1080,
        landing_zone=lz1,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    launch4_sr1 = StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
        stage=b1080,
        stage_position="MY",
        landing_zone=lz1,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    launch4_sr2 = StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
        stage=b1062,
        stage_position="PY",
        landing_zone=lz2,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    launch4_sr3 = StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
        stage=b1084,
        stage_position="CENTER",
        landing_zone=jrti,
        method="DRONE_SHIP",
        method_success="SUCCESS",
        recovery_success=True,
    )
    launch5_sr = StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon 9 Launch 4"),
        stage=b1080,
        landing_zone=jrti,
        method="DRONE_SHIP",
        method_success="SUCCESS",
        recovery_success=False,
    )

    SpacecraftOnLaunch.objects.create(
        launch=launch1, spacecraft=c206, splashdown_time=launch1.time + timedelta(days=14)
    )
    SpacecraftOnLaunch.objects.create(launch=launch2, spacecraft=c206)

    update_data()

    return {
        "spacex": spacex,
        "falcon_family": falcon_family,
        "falcon_9": falcon_9,
        "falcon_heavy": falcon_heavy,
        "dragon": dragon,
        "slc40": slc40,
        "lc39a": lc39a,
        "slc4e": slc4e,
        "low_earth_orbit": low_earth_orbit,
        "lz1": lz1,
        "lz2": lz2,
        "jrti": jrti,
        "b1062": b1062,
        "b1080": b1080,
        "b1084": b1084,
        "b1085": b1085,
        "launch1": launch1,
        "launch1_sr": launch1_sr,
        "launch2": launch2,
        "launch2_sr": launch2_sr,
        "launch3": launch3,
        "launch3_sr": launch3_sr,
        "launch4": launch4,
        "launch4_sr1": launch4_sr1,
        "launch4_sr2": launch4_sr2,
        "launch4_sr3": launch4_sr3,
        "launch5": launch5,
        "launch5_sr": launch5_sr,
        "c206": c206,
        "c207": c207,
    }


def update_data():
    for stage_and_recovery in StageAndRecovery.objects.all():
        stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
        stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
        stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
        stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
        stage_and_recovery.save(update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"])

    for launch in Launch.objects.all():
        launch.stages_string = launch.boosters
        launch.company_turnaround = launch.get_company_turnaround
        launch.pad_turnaround = launch.get_pad_turnaround
        launch.image = launch.get_image
        launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])

    for spacecraft_on_launch in SpacecraftOnLaunch.objects.all():
        spacecraft_on_launch._from_task = True
        spacecraft_on_launch.num_flights = spacecraft_on_launch.get_num_flights()
        spacecraft_on_launch.spacecraft_turnaround = spacecraft_on_launch.get_turnaround()
        spacecraft_on_launch.save(update_fields=["num_flights", "spacecraft_turnaround"])
        # Reset flag:
        spacecraft_on_launch._from_task = False
