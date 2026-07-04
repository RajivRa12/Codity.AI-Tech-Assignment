from django.db import transaction
from django.utils import timezone
from django.db.models import F, Q
from .models import Job, JobExecution, DeadLetter
import datetime

from django.conf import settings

def enqueue_job(queue, payload=None, job_type='immediate', scheduled_at=None, cron=None, batch_id=None, retry_policy=None, max_retries=3, created_by=None):
    payload = payload or {}
    job = Job.objects.create(
        queue=queue,
        type=job_type,
        payload=payload,
        scheduled_at=scheduled_at,
        cron=cron,
        batch_id=batch_id,
        retry_policy=retry_policy,
        max_retries=max_retries,
        created_by=created_by
    )
    if job_type == 'scheduled' or (job_type=='delayed' and scheduled_at):
        job.status = 'scheduled'
        job.save()
    return job

@transaction.atomic
def claim_next_job(queue=None):
    # Atomically claim a single queued job using select_for_update skip_locked
    now = timezone.now()
    qs = Job.objects.select_for_update(skip_locked=True).filter(status__in=['queued','scheduled'])
    if queue:
        qs = qs.filter(queue=queue)
    qs = qs.filter(Q(scheduled_at__lte=now) | Q(scheduled_at__isnull=True))
    job = qs.order_by('-queue__priority', 'created_at').first()
    if not job:
        return None
    job.status = 'claimed'
    job.attempts = F('attempts') + 1
    job.locked_at = now
    job.save()
    job.refresh_from_db()
    return job

def mark_running(job, worker):
    job.status = 'running'
    job.started_at = timezone.now()
    job.claimed_by = worker
    job.save()
    JobExecution.objects.create(job=job, worker=worker, attempt_number=job.attempts, status='running')
    # log
    try:
        from logs.services import log_job_event
        log_job_event(job=job, event_type='job.started', level='INFO', message='Job started', meta={'worker': getattr(worker,'name',None)})
    except Exception:
        pass

def mark_completed(job, result=None):
    job.status = 'completed'
    job.finished_at = timezone.now()
    job.result = result or {}
    job.save()
    JobExecution.objects.filter(job=job, attempt_number=job.attempts).update(status='completed', finished_at=timezone.now())
    try:
        from logs.services import log_job_event
        log_job_event(job=job, event_type='job.completed', level='INFO', message='Job completed', meta={'result': job.result})
    except Exception:
        pass

def mark_failed(job, error_message=''):
    job.status = 'failed'
    job.error_message = str(error_message)
    job.finished_at = timezone.now()
    job.save()
    JobExecution.objects.filter(job=job, attempt_number=job.attempts).update(status='failed', finished_at=timezone.now())
    # delegate retry scheduling to retry app
    try:
        from retry.services import schedule_retry
        scheduled = schedule_retry(job, str(error_message))
        if scheduled:
            return
    except Exception:
        pass
    DeadLetter.objects.create(job=job, reason=job.error_message)
    job.status = 'dead'
    job.save()
    try:
        from logs.services import log_job_event
        log_job_event(job=job, event_type='job.dead', level='ERROR', message='Moved to dead letter', meta={'error': job.error_message})
    except Exception:
        pass

def retry_job(job):
    if job.attempts < job.max_retries:
        job.status = 'queued'
        job.save()
        return True
    return False
