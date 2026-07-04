from rest_framework import permissions

class IsQueueOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser or getattr(user,'role','')=='admin':
            return True
        # for Job objects, check job.queue.project.created_by
        project = getattr(getattr(obj, 'queue', None), 'project', None) or getattr(obj, 'project', None)
        if project and getattr(project, 'created_by', None) == user:
            return True
        return False
