from django.core.mail import send_mail
from config import settings
from materials.models import CourseSubscribe, Course


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
