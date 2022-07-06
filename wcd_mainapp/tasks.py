from celery import shared_task
from wcd_mainapp.utils import periodic_task_handler, task_handler

@shared_task(bind=True)
def periodic_task_scheduler(self):
    periodic_task_handler()
    return "Working Perfectly"

@shared_task(bind=True)
def task_scheduler(self, id, url, type, threshold, css):
    task_handler(id, url, type, threshold, css)
    return "Working Perfectly"