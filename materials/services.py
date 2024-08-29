from datetime import timedelta, datetime
import pytz
from django.core.mail import send_mail
from config import settings
from materials.models import CourseSubscribe, Course
from users.models import User

ZONE = pytz.timezone(settings.TIME_ZONE)
NOW = datetime.now(ZONE)


def send_course_update_info(course_pk):
    course = Course.objects.filter(pk=course_pk).first()
    course_subscribes = CourseSubscribe.objects.filter(course=course)
    users_emails = [course_subscribe.user.email for course_subscribe in course_subscribes]

    send_mail(
        f'Курс {course} обновлен',
        f'Это сообщение является оповещением об обновлении курса {course}',
        settings.EMAIL_HOST_USER,
        users_emails,
        fail_silently=False
    )


def check_send_course_update():
    four_hours = NOW - timedelta(hours=4)

    courses_not_updated = Course.objects.filter(last_update__lte=four_hours)

    for course in courses_not_updated:
        send_course_update_info(course.pk)


def check_send_course_update():
    month = NOW - timedelta(days=28)

    users_not_active = User.objects.filter(last_login__lte=month)

    for user in users_not_active:
        if not user.is_staff or not user.is_superuser:
            user.is_active = False
            user.save()
