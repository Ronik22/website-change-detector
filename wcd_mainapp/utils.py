from loguru import logger
from wcd_mainapp.html_wcd import HtmlWCD
from wcd_mainapp.image_wcd import ImageWCD
from wcd_mainapp.text_wcd import TextWCD
from wcd_mainapp.models import Tasks


def task_handler(id, url, type, threshold=1.0, css="full"):
    if type == 1:
        ImageWCD(id, url, css, threshold).run()
    elif type ==2:
        HtmlWCD(id, url, css, threshold).run()
    elif type ==3:
        TextWCD(id, url, css, threshold).run()


def periodic_task_handler():
    logger.debug("periodic task handler started")
    all_tasks = Tasks.objects.all()
    for task in all_tasks:
        if task.detection_type == 1:
            try:
                ImageWCD(task.id, task.web_url, task.partOf, task.threshold).run()
                logger.success("Task-{} suceeded", task.id)
            except:
                logger.error("Task-{} failed", task.id)

        elif task.detection_type == 2:
            try:
                HtmlWCD(task.id, task.web_url, task.partOf, task.threshold).run()
                logger.success("Task-{} suceeded", task.id)
            except:
                logger.error("Task-{} failed", task.id)

        elif task.detection_type == 3:
            try:
                TextWCD(task.id, task.web_url, task.partOf, task.threshold).run()
                logger.success("Task-{} suceeded", task.id)
            except:
                logger.error("Task-{} failed", task.id)