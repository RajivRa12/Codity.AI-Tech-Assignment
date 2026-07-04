import re
from django.core.exceptions import ValidationError

CRON_RE = re.compile(r'^[^\n]+$')

def validate_cron(expr):
    if not expr or not CRON_RE.match(expr):
        raise ValidationError('Invalid cron expression')
    return expr
