import uuid
from django.db import models

class Queue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='queues')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.IntegerField(default=0)
    concurrency_limit = models.IntegerField(default=1)
    retry_policy = models.ForeignKey('retry.RetryPolicy', null=True, blank=True, on_delete=models.SET_NULL)
    is_paused = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority','name']
        indexes = [
            models.Index(fields=['project','priority']),
        ]

    def __str__(self):
        return f"{self.name} ({self.project})"
