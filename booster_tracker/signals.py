# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
from booster_tracker.models import (
    Stage,
    StageAndRecovery,
    Pad,
    Boat,
    Rocket,
    LandingZone,
    Launch,
    RocketFamily,
    SpacecraftFamily,
)
from django.template.loader import render_to_string
from booster_tracker.home_utils import (
    generate_home_page,
    generate_boosters_page,
    generate_starship_home,
    generate_spacecraft_list,
    StageObjects,
)

CACHE_KEYS = ["home_page", "starship_home", "Falcon_boosters", "Starship_boosters", "Dragons", "launches"]


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

    for cache_key in CACHE_KEYS:
        cache.delete(cache_key)
    regenerate_cache()


def regenerate_cache():
    # Cache home page:
    context = generate_home_page()

    cache_key = "home_page"
    cache.set(cache_key, context, timeout=None)

    # Cache boosters page:
    for rocket_family in RocketFamily.objects.all():
        context = generate_boosters_page(rocket_family=rocket_family, stage_type=StageObjects.BOOSTER)

        cache_key = f"{rocket_family.name.lower()}_boosters"
        cache.set(cache_key, context, timeout=None)

    # Cache Starship home:
    context = generate_starship_home()

    cache_key = "starship_home"
    cache.set(cache_key, context, timeout=None)

    # Cache Dragons list:
    for spacecraft_family in SpacecraftFamily.objects.all():
        context = generate_spacecraft_list(family=spacecraft_family)

        cache_key = f"{spacecraft_family}s"
        cache.set(cache_key, context, timeout=None)
