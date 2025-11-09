from datetime import timedelta

from celery import shared_task
from django.db.models import Count, Q
from django.utils import timezone

from .models import SuspiciousIP
from .models import RequestLog  # assumes Task 0 is done


SENSITIVE_PATHS = (
    "/admin",
    "/login",
    "/signin",
    "/auth",
    "/api/keys",
    "/settings",
)


@shared_task(bind=True, ignore_result=True)
def detect_anomalies(self):
    """
    Runs hourly to flag suspicious IPs:
    - >100 requests in the last hour
    - Any access to sensitive paths in the last hour
    """
    now = timezone.now()
    window_start = now - timedelta(hours=1)

    # 1) High request volume: >100 in the last hour
    high_volume = (
        RequestLog.objects
        .filter(timestamp__gte=window_start)
        .values("ip_address")
        .annotate(req_count=Count("id"))
        .filter(req_count__gt=100)
    )
    for row in high_volume:
        SuspiciousIP.objects.get_or_create(
            ip_address=row["ip_address"],
            reason="High volume (>100 req/hour)",
        )

    # 2) Sensitive paths accessed in the last hour
    q = Q()
    for prefix in SENSITIVE_PATHS:
        q |= Q(path__startswith=prefix)

    sensitive_hits = (
        RequestLog.objects
        .filter(timestamp__gte=window_start)
        .filter(q)
        .values_list("ip_address", flat=True)
        .distinct()
    )
    for ip in sensitive_hits:
        SuspiciousIP.objects.get_or_create(
            ip_address=ip,
            reason="Accessed sensitive path",
        )
