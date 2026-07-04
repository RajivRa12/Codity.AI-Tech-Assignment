from rest_framework import viewsets, permissions
from .models import RetryPolicy, RetryAttempt
from .serializers import RetryPolicySerializer, RetryAttemptSerializer

class RetryPolicyViewSet(viewsets.ModelViewSet):
    queryset = RetryPolicy.objects.all()
    serializer_class = RetryPolicySerializer
    permission_classes = (permissions.IsAuthenticated,)

class RetryAttemptViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RetryAttempt.objects.all()
    serializer_class = RetryAttemptSerializer
    permission_classes = (permissions.IsAuthenticated,)
