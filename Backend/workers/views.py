from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Worker
from .serializers import WorkerSerializer, HeartbeatSerializer
from .services import register_worker, detect_stale_workers
from .permissions import IsAdminOrWorker
from django.utils import timezone

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_permissions(self):
        if self.action in ['register','heartbeat']:
            return [permissions.IsAuthenticated(), IsAdminOrWorker()]
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['post'])
    def register(self, request):
        name = request.data.get('name') or request.data.get('hostname')
        hostname = request.data.get('hostname')
        pid = request.data.get('pid')
        concurrency = int(request.data.get('concurrency', 1))
        w = register_worker(name=name or 'worker', hostname=hostname, pid=pid, concurrency=concurrency)
        return Response(WorkerSerializer(w).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def heartbeat(self, request):
        name = request.data.get('name')
        try:
            w = Worker.objects.get(name=name)
        except Worker.DoesNotExist:
            return Response({'detail':'worker_not_registered'}, status=status.HTTP_404_NOT_FOUND)
        w.last_heartbeat = timezone.now()
        w.save()
        return Response({'status':'ok'})

    @action(detail=False, methods=['get'])
    def stale(self, request):
        workers = detect_stale_workers()
        return Response(WorkerSerializer(workers, many=True).data)
