from django.utils import timezone
from croniter import croniter
from .models import Schedule, ScheduleExecution
from jobs.services import enqueue_job
from django.db import transaction
import pytz
import datetime
from django.db import models


def schedule_pending_jobs(now=None):
    now = now or timezone.now()
    schedules = Schedule.objects.filter(is_active=True).filter(models.Q(next_run_at__lte=now) | models.Q(next_run_at__isnull=True))
    enqueued = []
    for s in schedules:
        try:
            # compute next run if missing
            if not s.next_run_at:
                base = s.last_run_at or now
                it = croniter(s.cron, base)
                next_dt = it.get_next(datetime.datetime)
                s.next_run_at = pytz.timezone(s.timezone).localize(next_dt).astimezone(pytz.UTC)
                s.save(update_fields=['next_run_at'])
            if s.next_run_at and s.next_run_at <= now:
                with transaction.atomic():
                    # prevent duplicate scheduling by checking last_run_at
                    if s.last_run_at and s.last_run_at >= s.next_run_at:
                        continue
                    # choose a queue: first project queue (caller should specify explicit queue in production)
                    queue = s.project.queues.first()
                    if not queue:
                        ScheduleExecution.objects.create(schedule=s, scheduled_for=s.next_run_at, status='failed', error='no_queue')
                        continue
                    job = enqueue_job(queue=queue, payload=s.payload, job_type='scheduled', created_by=s.created_by)
                    ScheduleExecution.objects.create(schedule=s, scheduled_for=s.next_run_at, enqueued_job=job, status='enqueued')
                    s.last_run_at = now
                    try:
                        from logs.services import log_schedule_event
                        log_schedule_event(s, event_type='schedule.enqueued', message='Schedule enqueued job', job=job)
                    except Exception:
                        pass
                    it = croniter(s.cron, s.next_run_at)
                    nxt = it.get_next(datetime.datetime)
                    s.next_run_at = pytz.timezone(s.timezone).localize(nxt).astimezone(pytz.UTC)
                    s.save(update_fields=['last_run_at','next_run_at'])
                    enqueued.append(job)
        except Exception as e:
            ScheduleExecution.objects.create(schedule=s, scheduled_for=s.next_run_at or now, status='failed', error=str(e))
    return enqueued
