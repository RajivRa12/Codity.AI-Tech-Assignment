from rest_framework import permissions

class IsProjectOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or getattr(user,'role','')=='admin':
            return True
        project = getattr(obj, 'project', None)
        if project and getattr(project, 'created_by', None) == user:
            return True
        return False
