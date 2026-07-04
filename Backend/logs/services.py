from .tasks import create_log_entry
from .models import LogEntry

def log_job_event(job=None, event_type='job.event', level='INFO', message='', meta=None, retry_attempt=None):
    payload = {
        'level': level,
        'event_type': event_type,
        'message': message,
        'job_id': str(job.id) if job else None,
        'worker_id': str(getattr(job,'claimed_by_id', None)) if job else None,
        'schedule_id': None,
        'retry_attempt_id': str(retry_attempt.id) if retry_attempt else None,
        'meta': meta or {},
    }
    try:
        create_log_entry.delay(payload)
    except Exception:
        # fallback to synchronous write
        LogEntry.objects.create(level=level, event_type=event_type, message=message, job=job, meta=meta or {})

def log_worker_heartbeat(worker, meta=None):
    payload = {
        'level':'INFO',
        'event_type':'worker.heartbeat',
        'message':f'Heartbeat from {worker.name}',
        'worker_id': str(worker.id),
        'meta': meta or {}
    }
    try:
        create_log_entry.delay(payload)
    except Exception:
        LogEntry.objects.create(level='INFO', event_type='worker.heartbeat', message=payload['message'], worker=worker, meta=meta or {})

def log_schedule_event(schedule, event_type='schedule.enqueued', message='', job=None, meta=None):
    payload = {
        'level':'INFO',
        'event_type':event_type,
        'message':message,
        'schedule_id': str(schedule.id) if schedule else None,
        'job_id': str(job.id) if job else None,
        'meta': meta or {}
    }
    try:
        create_log_entry.delay(payload)
    except Exception:
        LogEntry.objects.create(level='INFO', event_type=event_type, message=message, schedule=schedule, job=job, meta=meta or {})

def log_retry_attempt(retry_attempt, level='INFO', message=''):
    payload = {
        'level': level,
        'event_type': 'retry.attempt',
        'message': message,
        'retry_attempt_id': str(retry_attempt.id),
        'job_id': str(retry_attempt.job_id) if retry_attempt else None,
        'meta': {}
    }
    try:
        create_log_entry.delay(payload)
    except Exception:
        LogEntry.objects.create(level=level, event_type='retry.attempt', message=message, retry_attempt=retry_attempt)
