from celery import shared_task
from .models import LogEntry
from django.utils import timezone

@shared_task
def create_log_entry(payload):
    # payload is a dict matching LogEntry fields
    try:
        # pop unknown keys safely
        LogEntry.objects.create(
            level=payload.get('level','INFO'),
            event_type=payload.get('event_type','system'),
            message=payload.get('message',''),
            job_id=payload.get('job_id'),
            worker_id=payload.get('worker_id'),
            schedule_id=payload.get('schedule_id'),
            retry_attempt_id=payload.get('retry_attempt_id'),
            meta=payload.get('meta',{})
        )
    except Exception:
        # avoid raising from logging task
        return None
    return True
