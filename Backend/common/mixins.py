from django.db import models
from .models import TimeStampedModel

class TimeStampedModelMixin(TimeStampedModel):
    class Meta:
        abstract = True

class SoftDeleteMixin:
    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
