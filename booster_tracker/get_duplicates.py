import django
import os

import sys
print(sys.path)
sys.path.append("")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")
django.setup()

from django.core.management.base import BaseCommand
from booster_tracker.models import *
from django.db.models import Count



duplicates = (TugOnLaunch.objects.values('launch', 'boat').annotate(count=Count('id')).filter(count__gt=1))

for duplicate in duplicates:
    launch_id = duplicate['launch']
    launch_name = StageAndRecovery.objects.select_related('launch').get(launch=launch_id).launch.name

    print(f"Launch ID: {launch_name}")
    # Fetch all duplicates for this launch and stage
    # Keep the first record and delete the rest
