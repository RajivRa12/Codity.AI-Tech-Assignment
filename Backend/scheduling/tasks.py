from celery import shared_task
from .services import schedule_pending_jobs

@shared_task
def run_schedules():
    schedule_pending_jobs()
