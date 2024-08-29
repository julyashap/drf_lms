from celery import shared_task
from materials import services


@shared_task
def send_course_update_info(course_pk):
    services.send_course_update_info(course_pk)
