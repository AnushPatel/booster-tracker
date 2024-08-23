# tasks.py
from celery import shared_task
from booster_tracker.models import StageAndRecovery, Launch, Stage, SpacecraftOnLaunch
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


@shared_task
def update_cached_stageandrecovery_value_task(stage_id_list, zone_id):

    # Update all related StageAndRecovery instances
    related_stage_and_recoveries = StageAndRecovery.objects.filter(
        stage__id__in=stage_id_list, landing_zone__id=zone_id
    )
    for stage_and_recovery in related_stage_and_recoveries:
        stage_and_recovery._from_task = True
        stage_and_recovery.stage_turnaround = stage_and_recovery.get_stage_turnaround
        stage_and_recovery.zone_turnaround = stage_and_recovery.get_zone_turnaround
        stage_and_recovery.num_flights = stage_and_recovery.get_num_flights
        stage_and_recovery.num_recoveries = stage_and_recovery.get_num_landings
        stage_and_recovery.save(update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"])
        # Reset flag:
        stage_and_recovery._from_task = False

    related_launch_instances = Launch.objects.filter(stageandrecovery__stage__id__in=stage_id_list)
    for launch in related_launch_instances:
        launch._from_task = True
        launch.stages_string = launch.boosters
        launch.save(update_fields=["stages_string"])
        # Reset flag:
        launch._from_task = False


@shared_task
def update_cached_launch_value_task():

    # Update all related launch instances
    related_launches = Launch.objects.all()
    for launch in related_launches:
        launch._from_task = True
        launch.company_turnaround = launch.get_company_turnaround
        launch.pad_turnaround = launch.get_pad_turnaround
        launch.image = launch.get_image
        launch.stages_string = launch.boosters
        launch.save(update_fields=["company_turnaround", "pad_turnaround", "image", "stages_string"])
        launch._from_task = False


@shared_task
def update_cached_spacecraftonlaunch_value_task(spacecraft_id_list):
    # Update all related spacecraftonlaunch instances
    related_spacecraft_on_launches = SpacecraftOnLaunch.objects.filter(
        spacecraft__id__in=spacecraft_id_list,
    )
    for spacecraft_on_launch in related_spacecraft_on_launches:
        spacecraft_on_launch._from_task = True
        spacecraft_on_launch.num_flights = spacecraft_on_launch.get_num_flights()
        spacecraft_on_launch.spacecraft_turnaround = spacecraft_on_launch.get_turnaround()
        spacecraft_on_launch.save(update_fields=["num_flights", "spacecraft_turnaround"])
        # Reset flag:
        spacecraft_on_launch._from_task = False
