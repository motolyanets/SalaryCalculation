import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "salary_calculation.settings")
app = Celery("salary_calculation")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
