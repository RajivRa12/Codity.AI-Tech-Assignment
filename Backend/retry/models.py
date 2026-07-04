import uuid
from django.db import models

class RetryPolicy(models.Model):
    POLICY_TYPES = [('fixed','Fixed'),('linear','Linear'),('exponential','Exponential')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, unique=True)
    policy_type = models.CharField(max_length=32, choices=POLICY_TYPES)
    initial_delay_seconds = models.IntegerField(default=60)
    backoff_factor = models.FloatField(default=2.0)
    max_retries = models.IntegerField(default=3)
    jitter = models.BooleanField(default=False)
    conditions = models.JSONField(null=True, blank=True, help_text='Optional conditions to trigger retry (e.g., HTTP status codes)')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class RetryAttempt(models.Model):
    STATUS_CHOICES = [('scheduled','Scheduled'),('attempted','Attempted'),('failed','Failed'),('succeeded','Succeeded')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey('jobs.Job', on_delete=models.CASCADE, related_name='retry_attempts')
    policy = models.ForeignKey(RetryPolicy, on_delete=models.SET_NULL, null=True, blank=True)
    attempt_number = models.IntegerField(default=1)
    scheduled_for = models.DateTimeField(null=True, blank=True)
    executed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"RetryAttempt {self.job_id}#{self.attempt_number}"
