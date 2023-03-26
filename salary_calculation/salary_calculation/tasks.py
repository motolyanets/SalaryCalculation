from celery import shared_task

from django.core.mail import send_mail


@shared_task()
def send_result_email_task():
    send_mail(
        "Celery",
        "Celery работает!!!!!",
        "andrey.motolyanets@mail.ru",
        ["andrey.motolyanets@mail.ru"],
        fail_silently=False,
    )


