from django.db.models import Count

def get_queue_stats(queue):
    # Import jobs lazily to avoid circular imports before jobs app exists
    try:
        from jobs.models import Job
    except Exception:
        return {}
    stats = Job.objects.filter(queue=queue).aggregate(
        total=Count('id'),
    )
    return stats
