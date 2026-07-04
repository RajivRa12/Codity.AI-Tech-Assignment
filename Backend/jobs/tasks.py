from celery import shared_task
from .services import mark_completed, mark_failed
from .models import Job
from .services_executor import execute_payload

@shared_task(bind=True)
def execute_job_task(self, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return {'error':'job_not_found'}
    try:
        # Execute payload using executor service. mark_running should be called by the dispatcher that claimed the job.
        result = execute_payload(job.payload)
        mark_completed(job, result=result)
        return {'status':'completed'}
    except Exception as e:
        mark_failed(job, str(e))
        raise
