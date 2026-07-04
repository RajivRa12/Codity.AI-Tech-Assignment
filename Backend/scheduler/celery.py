import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scheduler.settings')
app = Celery('scheduler')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab
app.conf.beat_schedule = {
    'run-schedules-every-minute': {
        'task': 'scheduling.tasks.run_schedules',
        'schedule': crontab(minute='*/1')
    }
}
