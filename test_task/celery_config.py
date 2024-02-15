import os

from celery import Celery, shared_task

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_task.settings.local')

app = Celery('test_task')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.enable_utc = False
app.conf.timezone = "Europe/Moscow"

app.autodiscover_tasks()


@shared_task
def add(x, y):
    return x + y



