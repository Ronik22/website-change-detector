from loguru import logger
from wcd_mainapp.html_wcd import HtmlWCD
from wcd_mainapp.image_wcd import ImageWCD
from wcd_mainapp.text_wcd import TextWCD
from wcd_mainapp.models import Tasks
from django.core.mail import EmailMessage
from website_change_detector import settings

def task_handler(email, id, url, type, threshold=1.0, css="full"):
    if type == 1:
        info = ImageWCD(id, url, css, threshold).run()
    elif type == 2:
        info = HtmlWCD(id, url, css, threshold).run()
    elif type == 3:
        info = TextWCD(id, url, css, threshold).run()
    
    if info["ischanged"] and not info["firsttime"]:
        sendMail(email, info["website"], info["filepath"])


def periodic_task_handler(email):
    logger.debug("periodic task handler started")
    all_tasks = Tasks.objects.all()
    for task in all_tasks:
        if task.detection_type == 1:
            try:
                info = ImageWCD(task.id, task.web_url, task.partOf, task.threshold).run()
                logger.success("Task-{} suceeded", task.id)
            except:
                logger.error("Task-{} failed", task.id)

        elif task.detection_type == 2:
            try:
                info = HtmlWCD(task.id, task.web_url, task.partOf, task.threshold).run()
                logger.success("Task-{} suceeded", task.id)
            except:
                logger.error("Task-{} failed", task.id)

        elif task.detection_type == 3:
            try:
                info = TextWCD(task.id, task.web_url, task.partOf, task.threshold).run()
                logger.success("Task-{} suceeded", task.id)
            except:
                logger.error("Task-{} failed", task.id)

        if info["ischanged"] and not info["firsttime"]:
            sendMail(email, info["website"], info["filepath"])


def sendMail(to_email, website_name, filepath):
    subject = "Your website has changed"
    message = f"""
    Hello {to_email},<br><br>
    Your website ({website_name}) has changed. Please view the changes in the attached file below.<br><br>
    Thanks!!
    """
    try:
        mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [to_email])
        mail.content_subtype = "html"  
        mail.attach_file(filepath)
        mail.send()
        logger.success(f"Email sent to {to_email}")
    except:
        logger.error(f"Sending email to {to_email} failed.")