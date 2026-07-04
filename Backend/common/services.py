class BaseService:
    """Simple base service for business logic"""
    def __init__(self):
        pass

    def perform(self, *args, **kwargs):
        raise NotImplementedError
