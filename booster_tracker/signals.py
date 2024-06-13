# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from booster_tracker.models import (
    Stage,
    StageAndRecovery,
    Pad,
    Boat,
    Rocket,
    LandingZone,
    Launch,
)
from booster_tracker.tasks import invalidate_and_regenerate_cache


@receiver(post_save, sender=Stage)
@receiver(post_delete, sender=Stage)
@receiver(post_save, sender=StageAndRecovery)
@receiver(post_delete, sender=StageAndRecovery)
@receiver(post_save, sender=Pad)
@receiver(post_delete, sender=Pad)
@receiver(post_save, sender=Boat)
@receiver(post_delete, sender=Boat)
@receiver(post_save, sender=Rocket)
@receiver(post_delete, sender=Rocket)
@receiver(post_save, sender=LandingZone)
@receiver(post_delete, sender=LandingZone)
@receiver(post_save, sender=Launch)
@receiver(post_delete, sender=Launch)
def invalidate_cache(sender, instance, **kwargs):
    if settings.TESTING:
        return
    invalidate_and_regenerate_cache.delay()
