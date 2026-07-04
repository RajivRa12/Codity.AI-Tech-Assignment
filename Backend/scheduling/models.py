import uuid
from django.db import models
from django.conf import settings

class Schedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='schedules')
    name = models.CharField(max_length=255)
    cron = models.CharField(max_length=128)
    payload = models.JSONField(default=dict, blank=True)
    timezone = models.CharField(max_length=64, default='UTC')
    is_active = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    next_run_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('project','name'),)
        ordering = ['-created_at']

    def __str__(self):
        return f"Schedule {self.name} ({self.project})"

class ScheduleExecution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name='executions')
    scheduled_for = models.DateTimeField()
    enqueued_job = models.ForeignKey('jobs.Job', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=32, choices=[('enqueued','Enqueued'),('failed','Failed'),('skipped','Skipped')])
    created_at = models.DateTimeField(auto_now_add=True)
    error = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
