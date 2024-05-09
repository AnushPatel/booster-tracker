import django
import os

import sys
print(sys.path)
sys.path.append("")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")
django.setup()


from booster_tracker.models import *

def update_data():
    for stage in Stage.objects.all():
        status = "ACTIVE"
        for stageandrecovery in StageAndRecovery.objects.filter(stage=stage):
            if stageandrecovery.method == "EXPENDED":
                status = "EXPENDED"
            if (stageandrecovery.method == "GROUND_PAD" or stageandrecovery.method == "DRONE_SHIP") and stageandrecovery.recovery_success is False:
                status = "LOST"

        stage.status = status
        stage.save()

if __name__ == "__main__":
    update_data()
    print("RAN")