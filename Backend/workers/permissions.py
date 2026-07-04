from rest_framework import permissions

class IsAdminOrWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser or getattr(request.user,'role','')=='admin':
            return True
        return True  # allow authenticated users to register/check workers (tighten in production)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or getattr(request.user,'role','')=='admin':
            return True
        return False
