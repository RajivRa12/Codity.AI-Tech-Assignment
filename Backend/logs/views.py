from rest_framework import viewsets, permissions
from .models import LogEntry
from .serializers import LogEntrySerializer

class LogEntryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    permission_classes = (permissions.IsAuthenticated,)
    filterset_fields = ('level','event_type')
    search_fields = ('message','meta')
