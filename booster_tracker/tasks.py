# tasks.py
from celery import shared_task
from django.conf import settings
from booster_tracker.models import StageAndRecovery, Launch, Stage, SpacecraftOnLaunch
from booster_tracker.utils import make_x_post
from django.db.models import Q
import logging
from booster_tracker.fetch_data import fetch_nxsf_launches
from datetime import datetime, timedelta
from dateutil import parser
import pytz
import tweepy


logger = logging.getLogger(__name__)


@shared_task
def update_cached_stageandrecovery_value_task(stage_id_list, zone_id_list):

    # Update all related StageAndRecovery instances
    related_stage_and_recoveries = StageAndRecovery.objects.filter(
        Q(stage__id__in=stage_id_list) | Q(landing_zone__id__in=zone_id_list)
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
        launch.stages_string = launch.stages
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
        launch.stages_string = launch.stages
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


@shared_task
def update_launch_times():
    nxsf_data = fetch_nxsf_launches()
    now = datetime.now(pytz.utc)
    time_threshold = now - timedelta(hours=24)

    # Filter and parse launches where 'l' is 1 (SpaceX) and within the last 24 hours or in the future
    filtered_launches = []
    for launch in nxsf_data:
        if launch.get("l") == 1:
            launch_time = parser.parse(launch["t"]).astimezone(pytz.utc)
            if launch_time >= time_threshold:
                filtered_launches.append(launch)

    # Compare the launches and update the times
    for launch in Launch.objects.filter(time__gte=time_threshold).order_by("time"):
        nxsf_launch = next(
            (nxsf_launch for nxsf_launch in filtered_launches if nxsf_launch.get("n") == launch.name), None
        )
        if nxsf_launch:
            nxsf_launch_time = parser.parse(nxsf_launch["t"]).astimezone(pytz.utc)
            if nxsf_launch_time != launch.time:
                if nxsf_launch_time > launch.time + timedelta(hours=20):
                    launch.x_post_sent = False
                launch.time = nxsf_launch_time
                launch.save(update_fields=["time", "x_post_sent"])


@shared_task
def post_on_x(launch_id):
    launch = Launch.objects.get(id=launch_id)
    nxsf_launch = next((item for item in fetch_nxsf_launches() if item.get("n") == launch.name), None)

    if launch.x_post_sent or not nxsf_launch or launch.time != parser.parse(nxsf_launch["t"]).astimezone(pytz.utc):
        return

    post_string = launch.make_x_post()

    if settings.DEBUG:
        logger.info(f"Tweet: {post_string}")
    else:
        make_x_post(post_string=post_string)

    launch._from_task = True
    launch._is_updating_scheduled_post = True
    launch.x_post_sent = True
    launch.save(update_fields=["x_post_sent"])
    launch._from_task = False
    launch._is_updating_scheduled_post = False
