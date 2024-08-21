from datetime import datetime
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

    # Create pads
    pad1 = Pad.objects.create(
        name="Space Launch Complex 40",
        nickname="SLC-40",
        location="CCSFS",
        status="ACTIVE",
    )
    pad2 = Pad.objects.create(
        name="Launch Complex 39A",
        nickname="LC-39A",
        location="KSC",
        status="ACTIVE",
    )

    # Create orbit
    low_earth_orbit = Orbit.objects.create(name="low-Earth Orbit")

    # Create boats
    Boat.objects.create(name="Doug", type="SUPPORT")
    Boat.objects.create(name="Bob", type="SUPPORT")

    # Create landing zones
    lz1 = LandingZone.objects.create(name="Landing Zone 1", nickname="LZ-1", status="ACTIVE")
    lz2 = LandingZone.objects.create(name="Landing Zone 2", nickname="LZ-2", status="ACTIVE")
    jrt_i = LandingZone.objects.create(name="Just Read the Instructions", nickname="JRtI", status="ACTIVE")

    # Create stages
    stage1 = Stage.objects.create(
        name="B1062",
        rocket=falcon_9,
        version="v1.2 Block 5.4",
        type="BOOSTER",
        status="ACTIVE",
    )
    stage2 = Stage.objects.create(
        name="B1080",
        rocket=falcon_9,
        version="v1.2 Block 5.5",
        type="BOOSTER",
        status="ACTIVE",
    )
    stage3 = Stage.objects.create(
        name="B1084",
        rocket=falcon_heavy,
        version="v1.2 Block 5.5",
        type="BOOSTER",
        status="ACTIVE",
    )

    # Create pad usage
    PadUsed.objects.create(
        rocket=falcon_9,
        pad=pad1,
    )
    PadUsed.objects.create(
        rocket=falcon_heavy,
        pad=pad1,
    )
    PadUsed.objects.create(
        rocket=falcon_9,
        pad=pad2,
    )

    # Create launches
    Launch.objects.create(
        time=datetime(2024, 1, 1, 0, 0, tzinfo=pytz.utc),
        pad=pad1,
        rocket=falcon_9,
        name="Falcon 9 Launch 1",
        orbit=low_earth_orbit,
        mass="1000 kg",
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )
    Launch.objects.create(
        time=datetime(2024, 2, 1, tzinfo=pytz.utc),
        pad=pad1,
        rocket=falcon_9,
        name="Falcon 9 Launch 2",
        orbit=low_earth_orbit,
        mass="1000 kg",
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )
    Launch.objects.create(
        time=datetime(2024, 3, 1, tzinfo=pytz.utc),
        pad=pad1,
        rocket=falcon_9,
        name="Falcon 9 Launch 3",
        orbit=low_earth_orbit,
        mass="1000 kg",
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )
    Launch.objects.create(
        time=datetime(2024, 4, 1, tzinfo=pytz.utc),
        pad=pad1,
        rocket=falcon_heavy,
        name="Falcon Heavy Launch 1",
        orbit=low_earth_orbit,
        mass="1000 kg",
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )
    Launch.objects.create(
        time=datetime(2024, 5, 1, 0, 0, tzinfo=pytz.utc),
        pad=pad1,
        rocket=falcon_9,
        name="Falcon 9 Launch 4",
        orbit=low_earth_orbit,
        mass="1000 kg",
        customer="SpaceX",
        launch_outcome="SUCCESS",
    )

    # Create stage and recovery
    StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon 9 Launch 1"),
        stage=stage1,
        landing_zone=lz1,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon 9 Launch 2"),
        stage=stage1,
        landing_zone=lz1,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon 9 Launch 3"),
        stage=stage2,
        landing_zone=lz1,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
        stage=stage2,
        stage_position="MY",
        landing_zone=lz1,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
        stage=stage1,
        stage_position="PY",
        landing_zone=lz2,
        method="GROUND_PAD",
        method_success="SUCCESS",
        recovery_success=True,
    )
    StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon Heavy Launch 1"),
        stage=stage3,
        stage_position="CENTER",
        landing_zone=jrt_i,
        method="DRONE_SHIP",
        method_success="SUCCESS",
        recovery_success=True,
    )
    StageAndRecovery.objects.create(
        launch=Launch.objects.get(name="Falcon 9 Launch 4"),
        stage=stage2,
        method="EXPENDED",
        method_success="SUCCESS",
        recovery_success=False,
    )
