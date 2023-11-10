from celery import shared_task

from .utils import send_custom_email 


@shared_task
def send_email_via_celery(): 
    send_custom_email("This is a testing mail from celery.", " Please send a test email to the following locations to get started.", ["vijaythorat0804@gmail.com"])
    return True


@shared_task
def add(): 
    sum = 1+1
    return sum