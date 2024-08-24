# signals.py
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.db.models import Q
from booster_tracker.models import Stage, StageAndRecovery, Pad, Boat, Rocket, LandingZone, Launch, SpacecraftOnLaunch
from booster_tracker.tasks import (
    update_cached_stageandrecovery_value_task,
    update_cached_launch_value_task,
    update_cached_spacecraftonlaunch_value_task,
)


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
    update_cached_stageandrecovery_value_task.delay(stage_ids, landing_zone_ids)


@receiver(post_save, sender=Launch)
@receiver(post_delete, sender=Launch)
def updated_cached_launch_values(sender, instance, **kwargs):
    if getattr(instance, "_from_task", True):
        return

    update_cached_launch_value_task.delay()


@receiver(pre_save, sender=SpacecraftOnLaunch)
def cache_old_spacecraftonlaunch_values(sender, instance, **kwargs):
    if instance.pk:
        try:
            # Retrieve the current state before the update
            old_instance = SpacecraftOnLaunch.objects.get(pk=instance.pk)
            instance._old_spacecraft_id = old_instance.spacecraft.id
        except SpacecraftOnLaunch.DoesNotExist:
            instance._old_spacecraft_id = None


@receiver(post_save, sender=SpacecraftOnLaunch)
@receiver(post_delete, sender=SpacecraftOnLaunch)
def updated_cached_spacecraftonlaunch_values(sender, instance, **kwargs):
    if getattr(instance, "_from_task", True):
        return

    if hasattr(instance, "old_spacecraft_id"):
        update_cached_spacecraftonlaunch_value_task.delay([instance._old_spacecraft_id, instance.spacecraft.id])
    else:
        update_cached_spacecraftonlaunch_value_task.delay([instance.spacecraft.id])


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
