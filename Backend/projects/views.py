from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Organization, Project
from .serializers import OrganizationSerializer, ProjectSerializer, ProjectCreateSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """CRUD for Organizations. Owner is auto-set to the requesting user."""
    queryset = Organization.objects.select_related('owner').all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        # Users see only their own organizations (admins see all)
        user = self.request.user
        if user.role == 'admin':
            return super().get_queryset()
        return super().get_queryset().filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProjectViewSet(viewsets.ModelViewSet):
    """CRUD for Projects scoped to authenticated user's organizations."""
    queryset = Project.objects.select_related('organization', 'created_by').prefetch_related('queues').all()
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return ProjectCreateSerializer
        return ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return super().get_queryset()
        return super().get_queryset().filter(organization__owner=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
