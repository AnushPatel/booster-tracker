import django
import os
from booster_tracker.models import Stage, StageAndRecovery
import sys

print(sys.path)
sys.path.append("")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")
django.setup()


def update_data():
    for stage in Stage.objects.all():
        status = "ACTIVE"
        for stageandrecovery in StageAndRecovery.objects.filter(stage=stage):
            if stageandrecovery.method == "EXPENDED":
                status = "EXPENDED"
            if (
                stageandrecovery.method in ("GROUND_PAD", "DRONE_SHIP")
            ) and stageandrecovery.recovery_success is False:
                status = "LOST"

        stage.status = status
        stage.save()


if __name__ == "__main__":
    update_data()
    print("RAN")
