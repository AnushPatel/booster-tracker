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
    from django.templatetags.static import static
    from booster_tracker.home_utils import (
        get_next_and_last_launches,
        gather_launch_info,
        gather_stats,
        gather_pad_stats,
        gather_recovery_zone_stats,
    )

    next_launch, last_launch = get_next_and_last_launches()

    if not last_launch:
        return

    if next_launch:
        (
            next_launch_boosters,
            next_launch_recoveries,
            next_launch_tugs,
            next_launch_fairing_recovery,
            next_launch_photo,
        ) = gather_launch_info(next_launch)
    else:
        next_launch_boosters = "Unknown"
        next_launch_recoveries = ""
        next_launch_tugs = ""
        next_launch_fairing_recovery = ""
        next_launch_photo = static("images/falcon_9.jpg")

    (
        last_launch_boosters,
        last_launch_recoveries,
        last_launch_tugs,
        last_launch_fairing_recovery,
        _,
    ) = gather_launch_info(last_launch)

    stats = gather_stats(last_launch)
    pad_stats = gather_pad_stats(rocket_name="Falcon")
    recovery_zone_stats = gather_recovery_zone_stats(rocket_name="Falcon")

    context = {
        "launches_per_vehicle": stats["num_launches_per_rocket_and_successes"],
        "num_landings": stats["num_landings_and_successes"],
        "num_booster_reflights": stats["num_booster_reflights"],
        "next_launch": next_launch,
        "last_launch": last_launch,
        "next_launch_boosters": next_launch_boosters,
        "next_launch_recoveries": next_launch_recoveries,
        "next_launch_tugs": next_launch_tugs,
        "next_launch_fairing_recovery": next_launch_fairing_recovery,
        "next_launch_photo": next_launch_photo,
        "last_launch_boosters": last_launch_boosters,
        "last_launch_recoveries": last_launch_recoveries,
        "last_launch_tugs": last_launch_tugs,
        "last_launch_fairing_recovery": last_launch_fairing_recovery,
        "most_flown_boosters": stats["most_flown_boosters_string"],
        "quickest_booster_turnaround": stats["quickest_booster_turnaround_string"],
        "falcon_heavy_reflights": stats["falcon_heavy_reflights"],
        "falcon_9_reflights": stats["falcon_9_reflights"],
        "pad_stats": pad_stats,
        "zone_stats": recovery_zone_stats,
        "shortest_time_between_launches": stats["shortest_time_between_launches"],
    }

    rendered_content = render_to_string("launches/home.html", context)
    cache_key = "home_page"
    cache.set(cache_key, rendered_content, timeout=None)
