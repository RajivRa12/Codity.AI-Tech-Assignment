class ServiceError(Exception):
    """Base service exception"""
    pass

class NotFound(ServiceError):
    pass

class PermissionDenied(ServiceError):
    pass
