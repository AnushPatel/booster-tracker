import os
from django.conf import settings
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "launches_project.settings")

app = Celery("launches_project")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.worker_hijack_root_logger = False

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# this TASK_QUEUE_NAME will contain name of SQS queue and we'll define it later in settings.py
if not settings.DEBUG:
    app.conf.task_default_queue = settings.TASK_QUEUE_NAME
    app.conf.task_default_exchange = settings.TASK_QUEUE_NAME
    app.conf.task_default_routing_key = settings.TASK_QUEUE_NAME
