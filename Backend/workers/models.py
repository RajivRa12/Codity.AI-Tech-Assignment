import uuid
from django.db import models
from django.conf import settings

class Worker(models.Model):
    STATUS_CHOICES = [('online','Online'), ('draining','Draining'), ('offline','Offline')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    hostname = models.CharField(max_length=255, blank=True)
    pid = models.IntegerField(null=True, blank=True)
    concurrency = models.IntegerField(default=1)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='online')
    last_heartbeat = models.DateTimeField(null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=['status','last_heartbeat'])]

    def __str__(self):
        return f"{self.name} ({self.hostname})"

class WorkerHeartbeat(models.Model):
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, related_name='heartbeats')
    seen_at = models.DateTimeField(auto_now_add=True)
    meta = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-seen_at']
