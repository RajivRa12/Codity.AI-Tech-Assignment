import uuid
from django.utils.deprecation import MiddlewareMixin

class RequestIDMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.id = str(uuid.uuid4())

    def process_response(self, request, response):
        try:
            response['X-Request-ID'] = request.id
        except Exception:
            pass
        return response
