import django
import os

import sys
print(sys.path)
sys.path.append("")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")
django.setup()


from booster_tracker.models import *

def update_data():
    for instance in StageAndRecovery.objects.all():
        if instance.method_success:
            instance.method_success_2 = "SUCCESS"
        else:
            instance.method_success_2 = "FAILURE"
        instance.save()

if __name__ == "__main__":
    update_data()
    print("RAN")