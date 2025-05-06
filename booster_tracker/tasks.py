# tasks.py
from celery import shared_task
from django.conf import settings
from booster_tracker.models import StageAndRecovery, Launch, Stage, SpacecraftOnLaunch
from booster_tracker.utils import make_x_post
from django.db.models import Q
import logging
from booster_tracker.fetch_data import fetch_nxsf_boosters, fetch_nxsf_launches, fetch_nxsf_recovery
from datetime import datetime, timedelta
from dateutil import parser
import pytz
from django.db import transaction


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
    related_launches = Launch.objects.all().order_by("time")
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


# Configure logging
logger = logging.getLogger("Task Logger")
logger.setLevel(logging.INFO)  # Set the log level

# Create a console handler (optional, but good for immediate feedback)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for the console handler
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)


@shared_task
def get_nxsf_id(launch_id):
    try:
        launch_object = Launch.objects.get(id=launch_id)

        if launch_object.nxsf_id:
            return
        nxsf_data = fetch_nxsf_launches()

        for api_launch in nxsf_data:
            if api_launch.get("l") == 1 and api_launch.get("n") == launch_object.name:
                launch_object._from_task = True
                launch_object.nxsf_id = api_launch.get("i")
                launch_object.save(update_fields=["nxsf_id"])
                launch_object._from_task = False
                return
    except Launch.DoesNotExist:
        logger.error(f"Launch with ID {launch_id} does not exist.")
    except Exception as e:
        logger.error(f"Error fetching NXSF ID for launch {launch_id}: {e}")


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
            if nxsf_launch.get("s") == 4:
                current_day = now.date()
                next_day = current_day + timedelta(days=1)
                same_time = launch.time.time()
                updated_time = datetime.combine(next_day, same_time, tzinfo=pytz.utc)
            else:
                updated_time = nxsf_launch_time

            if updated_time != launch.time:
                if nxsf_launch_time > launch.time + timedelta(hours=20):
                    launch.x_post_sent = False
                launch.time = updated_time
                logger.info(f"saving launch {launch.name}")
                launch.save()


@shared_task
def update_recovery_status():
    recovery_data = fetch_nxsf_recovery()
    recovery_dict = {"Success": "SUCCESS", "Upcoming": "TBD", "Failure": "FAILURE"}

    for launch in Launch.objects.all():
        for recovery in recovery_data:
            if recovery.get("launch") == launch.nxsf_id:
                recovery_status = recovery.get("status")

                updated_status = recovery_dict[recovery_status]
                stage_recoveries = StageAndRecovery.objects.filter(launch=launch)

                for stage_recovery in stage_recoveries:
                    if stage_recovery.method_success != updated_status:
                        stage_recovery._from_task = True
                        stage_recovery.method_success = updated_status
                        stage_recovery.save(update_fields=["method_success"])
                        stage_recovery._from_task = False
                break


@shared_task
def update_launch_outcome():
    nxsf_api_data = fetch_nxsf_launches()

    outcome_dict = {6: "SUCCESS", 7: "PARTIAL FAILURE", 8: "FAILURE"}

    filtered_launches = []
    for launch in nxsf_api_data:
        if launch.get("l") == 1 and launch.get("s") in outcome_dict:
            launch_time = parser.parse(launch["t"]).astimezone(pytz.utc)
            if launch_time >= datetime.now(pytz.utc) - timedelta(hours=24):
                filtered_launches.append(launch)

    for nxsf_launch in filtered_launches:
        try:
            launch_name = nxsf_launch.get("n")
            status = nxsf_launch.get("s")
            outcome = outcome_dict.get(status)

            launch = Launch.objects.filter(
                name=launch_name, time__gte=datetime.now(pytz.utc) - timedelta(hours=24)
            ).first()

            if not launch:
                continue

            if launch.launch_outcome != outcome:
                launch._from_task = True
                launch.launch_outcome = outcome
                launch.save(update_fields=["launch_outcome"])
                launch._from_task = False

        except Exception as e:
            logger.error(f"Error updating launch outcome for {launch_name}: {e}")


@shared_task
def post_on_x(launch_id):
    launch = Launch.objects.get(id=launch_id)
    nxsf_launch = next((item for item in fetch_nxsf_launches() if item.get("n") == launch.name), None)
    time_delta_from_now = abs(launch.time - datetime.now(pytz.utc))

    if (
        launch.x_post_sent
        or not nxsf_launch
        or nxsf_launch.get("s") == 4
        or launch.time != parser.parse(nxsf_launch["t"]).astimezone(pytz.utc)
        or not time_delta_from_now <= timedelta(minutes=20)
    ):
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


@shared_task
def update_stage():
    recovery_data = fetch_nxsf_recovery()
    booster_data = fetch_nxsf_boosters()

    recent_launches = Launch.objects.filter(nxsf_id__isnull=False).order_by("-time")[:10]
    for launch in recent_launches:
        for recovery in recovery_data:
            if recovery.get("launch") == launch.nxsf_id:
                vehicle_id = recovery.get("vehicle")
                if not vehicle_id:
                    break

                booster_name = None
                for booster in booster_data:
                    if booster.get("id") == vehicle_id:
                        booster_name = booster.get("name")
                        break

                if not booster_name:
                    break

                for stage_recovery in StageAndRecovery.objects.filter(launch=launch):
                    if stage_recovery.stage and stage_recovery.stage.name == booster_name:
                        continue

                    rocket_id = None
                    if stage_recovery.stage and stage_recovery.stage.rocket_id:
                        rocket_id = stage_recovery.stage.rocket_id
                    elif launch.rocket_id:
                        rocket_id = launch.rocket_id
                    else:
                        continue

                    correct_stage = Stage.objects.filter(name=booster_name, rocket_id=rocket_id).first()

                    if not correct_stage:
                        continue

                    if (
                        StageAndRecovery.objects.filter(launch_id=launch.id, stage_id=correct_stage.id)
                        .exclude(id=stage_recovery.id)
                        .exists()
                    ):
                        continue
                    try:
                        stage_recovery.stage_id = correct_stage.id
                        stage_recovery.save()

                        # Manually trigger the update tasks that would normally be called by signals
                        stage_ids = [correct_stage.id]
                        update_cached_stageandrecovery_value_task.delay(stage_ids, [])
                        update_cached_launch_value_task.delay()
                    except Exception as e:
                        logger.error(f"Error updating stage recovery for launch {launch.id}: {e}")
                        continue

                break
