import threading
import time
from django.utils import timezone
from .models import Worker, WorkerHeartbeat
from jobs.services import claim_next_job, mark_running
from jobs.tasks import execute_job_task
from django.db import transaction

class WorkerRunner:
    """Simple runner that polls queues, claims jobs atomically, marks them running and dispatches to Celery."""
    def __init__(self, worker: Worker, poll_interval=5, stop_event=None):
        self.worker = worker
        self.poll_interval = poll_interval
        self.stop_event = stop_event or threading.Event()

    def heartbeat(self, meta=None):
        self.worker.last_heartbeat = timezone.now()
        self.worker.save(update_fields=['last_heartbeat'])
        WorkerHeartbeat.objects.create(worker=self.worker, meta=meta or {})
        try:
            from logs.services import log_worker_heartbeat
            log_worker_heartbeat(self.worker, meta=meta)
        except Exception:
            pass

    def run_once(self, queue):
        # Attempt to claim next job for a queue
        job = None
        with transaction.atomic():
            job = claim_next_job(queue)
            if not job:
                return None
            # mark running (sets started_at, creates execution)
            mark_running(job, self.worker)
        # dispatch to celery for execution
        execute_job_task.delay(str(job.id))
        return job

    def run(self, queues, concurrency=1):
        # loops over queues and claims jobs until stop_event set
        while not self.stop_event.is_set():
            self.heartbeat()
            sorted_queues = sorted(queues, key=lambda q: getattr(q, 'priority', 0), reverse=True)
            for q in sorted_queues:
                if self.stop_event.is_set():
                    break
                if getattr(q, 'is_paused', False):
                    continue
                # try to claim up to concurrency jobs per queue
                for _ in range(concurrency):
                    job = self.run_once(q)
                    if not job:
                        break
            time.sleep(self.poll_interval)

def register_worker(name, hostname=None, pid=None, concurrency=1):
    w, _ = Worker.objects.get_or_create(name=name, defaults={'hostname':hostname,'pid':pid,'concurrency':concurrency})
    w.hostname = hostname or w.hostname
    w.pid = pid or w.pid
    w.concurrency = concurrency
    w.status = 'online'
    w.last_heartbeat = timezone.now()
    w.save()
    WorkerHeartbeat.objects.create(worker=w)
    return w

def detect_stale_workers(timeout_seconds=60):
    cutoff = timezone.now() - timezone.timedelta(seconds=timeout_seconds)
    return Worker.objects.filter(last_heartbeat__lt=cutoff, status='online')
