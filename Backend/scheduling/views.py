from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Schedule, ScheduleExecution
from .serializers import ScheduleSerializer, ScheduleExecutionSerializer

class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def pause(self, request, pk=None):
        s = self.get_object()
        s.is_active = False
        s.save()
        return Response({'status':'paused'})

    @action(detail=True, methods=['post'])
    def resume(self, request, pk=None):
        s = self.get_object()
        s.is_active = True
        s.save()
        return Response({'status':'resumed'})

class ScheduleExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ScheduleExecution.objects.all()
    serializer_class = ScheduleExecutionSerializer
    permission_classes = (permissions.IsAuthenticated,)
