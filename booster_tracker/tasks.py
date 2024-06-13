# tasks.py
from celery import shared_task
from django.core.cache import cache
from booster_tracker.models import RocketFamily, SpacecraftFamily
from booster_tracker.home_utils import (
    generate_home_page,
    generate_boosters_page,
    generate_starship_home,
    generate_spacecraft_list,
    StageObjects,
)

CACHE_KEYS = ["home_page", "starship_home", "Falcon_boosters", "Starship_boosters", "Dragons", "launches"]


@shared_task
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


@shared_task
def invalidate_and_regenerate_cache():
    for cache_key in CACHE_KEYS:
        cache.delete(cache_key)
    regenerate_cache.delay()
