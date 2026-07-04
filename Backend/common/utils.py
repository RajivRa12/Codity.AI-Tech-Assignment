import os
from django.utils import timezone

def now_utc():
    return timezone.now()

def get_env(key, default=None):
    return os.environ.get(key, default)
