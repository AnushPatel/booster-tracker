# signals.py
from django.db.models.signals import post_save, post_delete, pre_save
from django.db import transaction
from django.dispatch import receiver
from datetime import timedelta, datetime
import pytz
from celery import current_app
from booster_tracker.models import Stage, StageAndRecovery, Pad, Boat, Rocket, LandingZone, Launch, SpacecraftOnLaunch
from booster_tracker.tasks import (
    get_nxsf_id,
    update_cached_stageandrecovery_value_task,
    update_cached_launch_value_task,
    update_cached_spacecraftonlaunch_value_task,
    post_on_x,
)
import logging

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


@receiver(pre_save, sender=StageAndRecovery)
def cache_old_stageandrecovery_values(sender, instance, **kwargs):
    if instance.pk:
        try:
            # Retrieve the current state before the update
            old_instance = StageAndRecovery.objects.get(pk=instance.pk)
            if old_instance.stage:
                instance._old_stage_id = old_instance.stage.id
            if old_instance.landing_zone:
                instance._old_landing_zone_id = old_instance.landing_zone.id
        except StageAndRecovery.DoesNotExist:
            instance._old_stage_id = None
            instance._old_landing_zone_id = None


@receiver(post_save, sender=StageAndRecovery)
@receiver(post_delete, sender=StageAndRecovery)
def updated_cached_stageandrecovery_values(sender, instance, **kwargs):
    if getattr(instance, "_from_task", True):
        return

    stage_ids = []
    landing_zone_ids = []

    # Check if stage exists and add its ID to the list
    if hasattr(instance, "stage") and instance.stage:
        stage_ids.append(instance.stage.id)
    if hasattr(instance, "_old_stage_id") and instance._old_stage_id:
        stage_ids.append(instance._old_stage_id)

    # Check if landing zone exists and add its ID to the list
    if hasattr(instance, "landing_zone") and instance.landing_zone:
        landing_zone_ids.append(instance.landing_zone.id)
    if hasattr(instance, "_old_landing_zone_id") and instance._old_landing_zone_id:
        landing_zone_ids.append(instance._old_landing_zone_id)

    # Pass the lists to the task, using empty lists if no IDs exist
    transaction.on_commit(lambda: update_cached_stageandrecovery_value_task.delay(stage_ids, landing_zone_ids))


@receiver(pre_save, sender=SpacecraftOnLaunch)
def cache_old_spacecraftonlaunch_values(sender, instance, **kwargs):
    if instance.pk:
        try:
            # Retrieve the current state before the update
            old_instance = SpacecraftOnLaunch.objects.get(pk=instance.pk)
            instance._old_spacecraft_id = old_instance.spacecraft.id
        except SpacecraftOnLaunch.DoesNotExist:
            instance._old_spacecraft_id = None


@receiver([post_save, post_delete], sender=SpacecraftOnLaunch)
def updated_cached_spacecraftonlaunch_values(sender, instance, **kwargs):
    if getattr(instance, "_from_task", True):
        return

    if hasattr(instance, "_old_spacecraft_id"):
        transaction.on_commit(
            lambda: update_cached_spacecraftonlaunch_value_task.delay(
                [instance._old_spacecraft_id, instance.spacecraft.id]
            )
        )
    else:
        transaction.on_commit(lambda: update_cached_spacecraftonlaunch_value_task.delay([instance.spacecraft.id]))


@receiver(pre_save, sender=Launch)
def store_original_time(sender, instance, **kwargs):
    if instance.pk:
        try:
            # Fetch the current instance from the database to get the original time
            old_instance = Launch.objects.get(pk=instance.pk)
            instance._original_time = old_instance.time
        except sender.DoesNotExist:
            instance._original_time = None
    else:
        instance._original_time = None


@receiver([post_save, post_delete], sender=Launch)
def handle_launch_signals(sender, instance: Launch, **kwargs):
    # Avoid infinite loop by skipping if already processing from a task
    if instance._from_task or instance._is_updating_scheduled_post:
        return

    transaction.on_commit(lambda: update_cached_launch_value_task.delay())

    if hasattr(instance, "_original_time") and instance._original_time != instance.time:
        stage_ids = list(StageAndRecovery.objects.filter(launch=instance).values_list("stage_id", flat=True))
        zone_ids = list(StageAndRecovery.objects.filter(launch=instance).values_list("landing_zone_id", flat=True))
        spacecraft_ids = list(
            SpacecraftOnLaunch.objects.filter(launch=instance).values_list("spacecraft_id", flat=True)
        )
        if stage_ids or zone_ids:
            transaction.on_commit(lambda: update_cached_stageandrecovery_value_task.delay(stage_ids, zone_ids))
        if spacecraft_ids:
            transaction.on_commit(lambda: update_cached_spacecraftonlaunch_value_task.delay(spacecraft_ids))

    if kwargs.get("signal") == post_save:
        # Check if the time field has changed
        if hasattr(instance, "_original_time") and instance._original_time == instance.time:
            return  # Time has not changed, so skip scheduling logic

        # Handle cache update and scheduling
        if instance.time >= datetime.now(pytz.utc) - timedelta(hours=1):
            pre_save.disconnect(store_original_time, sender=Launch)
            instance._from_task = True
            instance._is_updating_scheduled_post = True

            # Cancel the existing scheduled task, if any
            logger.info(f"Old Task id: {instance.celery_task_id}")
            if instance.celery_task_id:
                current_app.control.revoke(instance.celery_task_id, terminate=True)
                logger.info(f"Revoked {instance.celery_task_id}")

            # Schedule a new task 15 minutes before launch time
            post_time = instance.time - timedelta(minutes=15)
            task = post_on_x.apply_async((instance.id,), eta=post_time)

            # Store the task ID for future reference
            instance.celery_task_id = task.id
            instance.save(update_fields=["celery_task_id"])
            logger.info(f"New Task id: {instance.celery_task_id}")
            instance._from_task = False
            instance._is_updating_scheduled_post = False
            pre_save.connect(store_original_time, sender=Launch)

    elif kwargs.get("signal") == post_delete:
        # Handle task revocation for deletions
        if instance.celery_task_id:
            current_app.control.revoke(instance.celery_task_id, terminate=True)
            logger.info(f"Revoked {instance.celery_task_id}")


@receiver(post_save, sender=Launch)
def trigger_nxsf_id_update(sender, instance, created, **kwargs):
    # Avoid infinite loop by checking if this is from a task
    if getattr(instance, "_from_task", False) or getattr(instance, "_is_updating_scheduled_post", False):
        return
    # Schedule the task to run after transaction commit
    transaction.on_commit(lambda: get_nxsf_id.delay(instance.id))
    logger.info(f"Scheduled NXSF ID update after {'creation' if created else 'update'} of Launch {instance.name}")
    logger.info(f"Launch {instance.name} NXSF ID: {instance.nxsf_id}")


""" @receiver(post_save, sender=Launch)
@receiver(post_delete, sender=Launch)
def updated_cached_launch_values(sender, instance, **kwargs):
    post_save.disconnect(updated_cached_launch_values, sender=Launch)
    post_delete.disconnect(updated_cached_launch_values, sender=Launch)

    try:
        instance.image = instance.get_image
        instance.save(
            update_fields=[
                "image",
            ]
        )

    finally:
        # Reconnect signals after the update
        post_save.connect(updated_cached_launch_values, sender=Launch)
        post_delete.connect(updated_cached_launch_values, sender=Launch) """
