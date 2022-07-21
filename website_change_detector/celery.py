from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from website_change_detector import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_change_detector.settings')

app = Celery('website_change_detector')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')

# Celery beat
app.conf.beat_schedule = {
    'website-change-detection': {
        'task': 'wcd_mainapp.tasks.periodic_task_scheduler',
        'schedule': crontab(minute=settings.CELERY_BEAT_CRONTAB_SCHEDULE),
    },
} 

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))