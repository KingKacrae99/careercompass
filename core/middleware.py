import logging

logger = logging.getLogger(__name__)

class logRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT", "Unknown")

        logger.info(f'Request from IP Address: {ip_address}, User-Agent: {user_agent}')

        response = self.get_response(request)

        logger.info(f"Response status: {response.status_code}")

        return response