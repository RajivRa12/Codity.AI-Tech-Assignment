from django.utils import timezone
import datetime
from .models import RetryPolicy, RetryAttempt

def compute_next_delay(policy: RetryPolicy, attempt_number: int) -> int:
    base = policy.initial_delay_seconds
    if policy.policy_type == 'fixed':
        delay = base
    elif policy.policy_type == 'linear':
        delay = base * attempt_number
    elif policy.policy_type == 'exponential':
        delay = int(base * (policy.backoff_factor ** (attempt_number - 1)))
    else:
        delay = base
    return int(delay)

def schedule_retry(job, error_message=''):
    policy = getattr(job, 'retry_policy', None)
    if not policy:
        if job.attempts >= job.max_retries:
            return False
        delay = 60
    else:
        attempt_no = job.attempts
        if attempt_no >= policy.max_retries:
            return False
        delay = compute_next_delay(policy, attempt_no)
    scheduled_for = timezone.now() + datetime.timedelta(seconds=delay)
    try:
        ra = RetryAttempt.objects.create(job=job, policy=policy, attempt_number=job.attempts + 1, scheduled_for=scheduled_for, status='scheduled', error_message=error_message)
    except Exception:
        ra = None
    job.scheduled_at = scheduled_for
    job.status = 'scheduled'
    job.save()
    try:
        from logs.services import log_retry_attempt
        if ra:
            log_retry_attempt(ra, level='INFO', message='Scheduled retry')
    except Exception:
        pass
    return True
