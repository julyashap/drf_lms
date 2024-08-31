from celery import shared_task
from users import services


@shared_task
def is_user_active():
    services.is_user_active()
