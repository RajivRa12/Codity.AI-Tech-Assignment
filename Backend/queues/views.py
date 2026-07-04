from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Queue
from .serializers import QueueSerializer
from .permissions import IsProjectOwnerOrAdmin


class QueueViewSet(viewsets.ModelViewSet):
    """Manage job queues. Supports pause, resume, and statistics."""
    queryset = Queue.objects.select_related('project', 'retry_policy').all()
    serializer_class = QueueSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['priority', 'created_at', 'name']

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'admin':
            return qs
        return qs.filter(project__organization__owner=user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'pause', 'resume']:
            return [permissions.IsAuthenticated(), IsProjectOwnerOrAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        """Pause a queue — workers will stop picking up new jobs."""
        queue = self.get_object()
        queue.is_paused = True
        queue.save(update_fields=['is_paused', 'updated_at'])
        return Response({'status': 'paused', 'queue_id': str(queue.id)}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        """Resume a paused queue."""
        queue = self.get_object()
        queue.is_paused = False
        queue.save(update_fields=['is_paused', 'updated_at'])
        return Response({'status': 'resumed', 'queue_id': str(queue.id)}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Return job counts grouped by status for this queue."""
        queue = self.get_object()
        from jobs.models import Job
        counts = (
            Job.objects.filter(queue=queue)
            .values('status')
            .annotate(count=Count('id'))
        )
        stats_dict = {item['status']: item['count'] for item in counts}
        total = sum(stats_dict.values())
        return Response({
            'queue_id': str(queue.id),
            'queue_name': queue.name,
            'is_paused': queue.is_paused,
            'total_jobs': total,
            'by_status': {
                'queued': stats_dict.get('queued', 0),
                'scheduled': stats_dict.get('scheduled', 0),
                'claimed': stats_dict.get('claimed', 0),
                'running': stats_dict.get('running', 0),
                'completed': stats_dict.get('completed', 0),
                'failed': stats_dict.get('failed', 0),
                'dead': stats_dict.get('dead', 0),
            },
        })
