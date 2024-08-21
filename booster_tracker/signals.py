# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.db.models import Q
from booster_tracker.models import Stage, StageAndRecovery, Pad, Boat, Rocket, LandingZone, Launch, SpacecraftOnLaunch


@receiver(post_save, sender=StageAndRecovery)
@receiver(post_delete, sender=StageAndRecovery)
def updated_cached_stageandrecovery_values(sender, instance, **kwargs):
    post_save.disconnect(updated_cached_stageandrecovery_values, sender=StageAndRecovery)
    post_delete.disconnect(updated_cached_stageandrecovery_values, sender=StageAndRecovery)

    try:
        # Update all related StageAndRecovery instances
        related_instances = StageAndRecovery.objects.filter(
            Q(stage=instance.stage) | Q(landing_zone=instance.landing_zone)
        )
        updated_ids = set()
        for instance in related_instances:
            if instance.id not in updated_ids:
                instance.stage_turnaround = instance.get_stage_turnaround
                instance.zone_turnaround = instance.get_zone_turnaround
                instance.num_flights = instance.get_num_flights
                instance.num_recoveries = instance.get_num_landings
                instance.save(update_fields=["stage_turnaround", "zone_turnaround", "num_flights", "num_recoveries"])
                updated_ids.add(instance.id)
    finally:
        # Reconnect signals after the update
        post_save.connect(updated_cached_stageandrecovery_values, sender=StageAndRecovery)
        post_delete.connect(updated_cached_stageandrecovery_values, sender=StageAndRecovery)


@receiver(post_save, sender=Launch)
@receiver(post_delete, sender=Launch)
def updated_cached_launch_values(sender, instance, **kwargs):
    post_save.disconnect(updated_cached_launch_values, sender=Launch)
    post_delete.disconnect(updated_cached_launch_values, sender=Launch)

    try:
        # Update all related StageAndRecovery instances
        related_instances = Launch.objects.all()
        updated_names = set()
        for instance in related_instances:
            if instance.name not in updated_names:
                instance.company_turnaround = instance.get_company_turnaround
                instance.pad_turnaround = instance.get_pad_turnaround
                instance.stages_string = instance.boosters
                instance.launch_photo = instance.image
                instance.save(update_fields=["company_turnaround", "pad_turnaround", "stages_string", "launch_photo"])
                updated_names.add(instance.name)
    finally:
        # Reconnect signals after the update
        post_save.connect(updated_cached_launch_values, sender=Launch)
        post_delete.connect(updated_cached_launch_values, sender=Launch)


@receiver(post_save, sender=SpacecraftOnLaunch)
@receiver(post_delete, sender=SpacecraftOnLaunch)
def updated_cached_spacecraftonlaunch_values(sender, instance, **kwargs):
    post_save.disconnect(updated_cached_spacecraftonlaunch_values, sender=SpacecraftOnLaunch)
    post_delete.disconnect(updated_cached_spacecraftonlaunch_values, sender=SpacecraftOnLaunch)

    try:
        # Update all related StageAndRecovery instances
        related_instances = SpacecraftOnLaunch.objects.filter(spacecraft=instance.spacecraft)
        updated_ids = set()
        for instance in related_instances:
            if instance.id not in updated_ids:
                instance.num_flights = instance.get_num_flights()
                instance.spacecraft_turnaround = instance.get_turnaround()
                instance.save(update_fields=["num_flights", "spacecraft_turnaround"])
                updated_ids.add(instance.id)
    finally:
        # Reconnect signals after the update
        post_save.connect(updated_cached_spacecraftonlaunch_values, sender=SpacecraftOnLaunch)
        post_delete.connect(updated_cached_spacecraftonlaunch_values, sender=SpacecraftOnLaunch)


""" @receiver(post_save, sender=Launch)
@receiver(post_delete, sender=Launch)
def updated_cached_launch_values(sender, instance, **kwargs):
    post_save.disconnect(updated_cached_launch_values, sender=Launch)
    post_delete.disconnect(updated_cached_launch_values, sender=Launch)

    try:
        instance.launch_photo = instance.image
        instance.save(
            update_fields=[
                "launch_photo",
            ]
        )

    finally:
        # Reconnect signals after the update
        post_save.connect(updated_cached_launch_values, sender=Launch)
        post_delete.connect(updated_cached_launch_values, sender=Launch) """
