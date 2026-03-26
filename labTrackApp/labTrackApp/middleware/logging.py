import logging
from django.utils import timezone

logger = logging.getLogger('django')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # logic executed before Request is passed to the View(or any othee middleware)

        start_time = timezone.now()

        logger.info(
            f"INCOMING | Path: {request.path} | Method: {request.method} | User: {request.user}"
        )

        response = self.get_response(request)

        # logic executed after view is called

        end_time = timezone.now()
        duration = (end_time - start_time).total_seconds()
        
        # log outgoing response details
        logger.info(
            f"OUTGOING | Status: {response.status_code} | Duration: {duration:.4f}s | Path: {request.path}"
        )

        return response