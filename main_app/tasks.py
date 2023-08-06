from celery import shared_task
from django.core.mail import send_mail

from django.conf import settings


@shared_task
def send_message_a_course_update(course_title, version, user_email):
    """Отправка письма пользователям об обновлении материалов курса."""

    send_mail(
        subject=f"Обновление курса!",
        message=f"У курса {course_title} появилось обновление - {version}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email]
    )