import logging

logger = logging.getLogger(__name__)


class HttpTrafficLogger:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Log network traffic
        logger.info(f"Request: {request.method} {request.path}")
        logger.info(f"Response status: {response.status_code}")

        return response
