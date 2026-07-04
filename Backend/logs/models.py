import uuid
from django.db import models

class LogEntry(models.Model):
    LEVEL_CHOICES = [('DEBUG','DEBUG'),('INFO','INFO'),('WARNING','WARNING'),('ERROR','ERROR')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    level = models.CharField(max_length=16, choices=LEVEL_CHOICES, default='INFO', db_index=True)
    event_type = models.CharField(max_length=128, db_index=True)
    message = models.TextField(blank=True)
    job = models.ForeignKey('jobs.Job', null=True, blank=True, on_delete=models.SET_NULL, related_name='logs')
    worker = models.ForeignKey('workers.Worker', null=True, blank=True, on_delete=models.SET_NULL, related_name='logs')
    schedule = models.ForeignKey('scheduling.Schedule', null=True, blank=True, on_delete=models.SET_NULL, related_name='logs')
    retry_attempt = models.ForeignKey('retry.RetryAttempt', null=True, blank=True, on_delete=models.SET_NULL, related_name='logs')
    meta = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [models.Index(fields=['level','event_type','timestamp'])]

    def __str__(self):
        return f"[{self.level}] {self.event_type} @ {self.timestamp}"
