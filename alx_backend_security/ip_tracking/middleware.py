from .models import RequestLog
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

class IPLoggingMiddleware(MiddlewareMixin):
    def get_client_ip(self, request):
        # Try to extract real IP even behind proxies
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        ip = self.get_client_ip(request)
        path = request.path
        RequestLog.objects.create(
            ip_address=ip,
            path=path,
            timestamp=timezone.now()
        )
