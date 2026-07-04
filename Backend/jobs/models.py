import uuid
from django.db import models
from django.conf import settings
# Use Django's built-in JSONField

class Job(models.Model):
    JOB_TYPES = [('immediate','Immediate'),('delayed','Delayed'),('scheduled','Scheduled'),('recurring','Recurring'),('batch','Batch')]
    STATUS_CHOICES = [
        ('queued','Queued'),('scheduled','Scheduled'),('claimed','Claimed'),('running','Running'),('completed','Completed'),('failed','Failed'),('dead','DeadLetter')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    queue = models.ForeignKey('queues.Queue', on_delete=models.CASCADE, related_name='jobs')
    type = models.CharField(max_length=32, choices=JOB_TYPES, default='immediate')
    payload = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='queued', db_index=True)
    scheduled_at = models.DateTimeField(null=True, blank=True, db_index=True)
    cron = models.CharField(max_length=128, blank=True, null=True)
    batch_id = models.UUIDField(null=True, blank=True, db_index=True)
    attempts = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    retry_policy = models.ForeignKey('retry.RetryPolicy', null=True, blank=True, on_delete=models.SET_NULL)
    claimed_by = models.ForeignKey('workers.Worker', null=True, blank=True, on_delete=models.SET_NULL)
    locked_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['queue','status']), models.Index(fields=['scheduled_at'])]
        ordering = ['-created_at']

    def __str__(self):
        return f"Job {self.id} ({self.type})"

class JobExecution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='executions')
    worker = models.ForeignKey('workers.Worker', null=True, blank=True, on_delete=models.SET_NULL)
    attempt_number = models.IntegerField(default=1)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, choices=Job.STATUS_CHOICES)
    runtime_seconds = models.FloatField(null=True, blank=True)
    logs = models.TextField(blank=True)

    class Meta:
        ordering = ['-started_at']

class DeadLetter(models.Model):
    job = models.OneToOneField(Job, on_delete=models.CASCADE, related_name='dead_letter')
    reason = models.TextField()
    moved_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"DeadLetter for {self.job_id}"

class ScheduledJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='scheduled_jobs')
    name = models.CharField(max_length=255)
    cron = models.CharField(max_length=128)
    payload = models.JSONField(default=dict, blank=True)
    timezone = models.CharField(max_length=64, default='UTC')
    is_active = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"ScheduledJob {self.name}"
