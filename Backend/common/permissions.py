from rest_framework import permissions
from .constants import ROLE_ADMIN

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = getattr(request, 'user', None)
        return bool(user and (user.is_superuser or getattr(user, 'role', None) == ROLE_ADMIN))

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.is_superuser or getattr(user,'role','') == ROLE_ADMIN:
            return True
        owner = getattr(obj, 'created_by', None) or getattr(obj, 'owner', None)
        return owner == user
