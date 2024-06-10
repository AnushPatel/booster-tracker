# signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from django.conf import settings
from booster_tracker.models import Stage, StageAndRecovery, Pad, Boat, Rocket, LandingZone, Launch


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

    cache_key = "home_page"
    cache.delete(cache_key)
    regenerate_cache()


def regenerate_cache():
    from django.template.loader import render_to_string
    from booster_tracker.home_utils import generate_home_page

    context = generate_home_page()

    rendered_content = render_to_string("launches/home.html", context)
    cache_key = "home_page"
    cache.set(cache_key, rendered_content, timeout=None)
