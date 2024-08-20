import django
import os
import sys

sys.path.append("")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")
django.setup()

from booster_tracker.models import Launch, StageAndRecovery, SpacecraftOnLaunch

# def update_data():
#     for stage in Stage.objects.all():
#         status = "ACTIVE"
#         for stageandrecovery in StageAndRecovery.objects.filter(stage=stage):
#             if stageandrecovery.method == "EXPENDED":
#                 status = "EXPENDED"
#             if (
#                 stageandrecovery.method in ("GROUND_PAD", "DRONE_SHIP")
#             ) and stageandrecovery.recovery_success is False:
#                 status = "LOST"

#         stage.status = status
#         stage.save()


# Before running these on database, comment out receiver in signals.py
def update_cached_data():
    stage_and_recoveries = StageAndRecovery.objects.all()
    for stageandrecovery in stage_and_recoveries:
        stageandrecovery.stage_turnaround = stageandrecovery.get_stage_turnaround
        stageandrecovery.num_flights = stageandrecovery.get_num_flights
        stageandrecovery.zone_turnaround = stageandrecovery.get_zone_turnaround
        stageandrecovery.num_recoveries = stageandrecovery.get_num_landings

        stageandrecovery.save(update_fields=["stage_turnaround", "num_flights", "num_recoveries", "zone_turnaround"])

    for launch in Launch.objects.all():
        launch.pad_turnaround = launch.get_pad_turnaround
        launch.company_turnaround = launch.get_company_turnaround

        launch.save(update_fields=["pad_turnaround", "company_turnaround"])

    for spacecraftonlaunch in SpacecraftOnLaunch.objects.all():
        spacecraftonlaunch.num_flights = spacecraftonlaunch.get_num_flights()
        spacecraftonlaunch.spacecraft_turnaround = spacecraftonlaunch.get_turnaround()

        spacecraftonlaunch.save(update_fields=["num_flights", "spacecraft_turnaround"])


if __name__ == "__main__":
    update_cached_data()
    print("RAN")
