from django_ratelimit.decorators import ratelimit
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


def get_client_ip(request):
    """Extract client IP from request, considering proxies."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@swagger_auto_schema(
    method="post",
    operation_description="Anonymous login endpoint with rate limiting (5 requests per minute per IP)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Username"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Password"
            ),
        },
        required=["username", "password"],
    ),
    responses={
        200: openapi.Response(
            description="Successful login attempt",
            examples={
                "application/json": {
                    "status": "success",
                    "message": "Login attempt recorded",
                    "ip_address": "192.168.1.1",
                }
            },
        ),
        429: openapi.Response(
            description="Rate limit exceeded",
            examples={
                "application/json": {"error": "Rate limit exceeded. Try again later."}
            },
        ),
    },
    tags=["Authentication"],
)
@api_view(["POST"])
@permission_classes([AllowAny])
@ratelimit(key="ip", rate="5/m", method="POST", block=True)
def anonymous_sensitive_view(request):
    """
    Handle anonymous login attempts with IP-based rate limiting.
    Limited to 5 requests per minute per IP address.
    """
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return Response({"error": "Rate limit exceeded. Try again later."}, status=429)

    ip_address = get_client_ip(request)

    # Your login logic here
    # For demo purposes, just return success
    return Response(
        {
            "status": "success",
            "message": "Login attempt recorded",
            "ip_address": ip_address,
            "rate_limit_info": {"limit": "5 requests per minute", "method": "IP-based"},
        }
    )


@swagger_auto_schema(
    method="post",
    operation_description="Authenticated user login endpoint with rate limiting (10 requests per minute per user)",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "username": openapi.Schema(
                type=openapi.TYPE_STRING, description="Username"
            ),
            "password": openapi.Schema(
                type=openapi.TYPE_STRING, description="Password"
            ),
        },
        required=["username", "password"],
    ),
    responses={
        200: openapi.Response(
            description="Successful login attempt",
            examples={
                "application/json": {
                    "status": "success",
                    "message": "Authenticated login attempt recorded",
                    "user": "john_doe",
                    "ip_address": "192.168.1.1",
                }
            },
        ),
        401: openapi.Response(
            description="Unauthorized - Authentication required",
        ),
        429: openapi.Response(
            description="Rate limit exceeded",
            examples={
                "application/json": {"error": "Rate limit exceeded. Try again later."}
            },
        ),
    },
    tags=["Authentication"],
    security=[{"Bearer": []}],
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
@ratelimit(key="user", rate="10/m", method="POST", block=True)
def authenticated_sensitive_view(request):
    """
    Handle authenticated login attempts with user-based rate limiting.
    Limited to 10 requests per minute per authenticated user.
    Requires authentication token.
    """
    was_limited = getattr(request, "limited", False)

    if was_limited:
        return Response({"error": "Rate limit exceeded. Try again later."}, status=429)

    ip_address = get_client_ip(request)
    username = request.user.username

    # Your authenticated login logic here
    return Response(
        {
            "status": "success",
            "message": "Authenticated login attempt recorded",
            "user": username,
            "ip_address": ip_address,
            "rate_limit_info": {
                "limit": "10 requests per minute",
                "method": "User-based",
            },
        }
    )


@swagger_auto_schema(
    method="get",
    operation_description="Get current user information and rate limit status",
    responses={
        200: openapi.Response(
            description="User information",
            examples={
                "application/json": {
                    "user": "john_doe",
                    "ip_address": "192.168.1.1",
                    "is_authenticated": True,
                }
            },
        ),
    },
    tags=["User Info"],
)
@api_view(["GET"])
@permission_classes([AllowAny])
def user_info_view(request):
    """Get current user information and IP address."""
    ip_address = get_client_ip(request)

    return Response(
        {
            "user": (
                request.user.username if request.user.is_authenticated else "anonymous"
            ),
            "ip_address": ip_address,
            "is_authenticated": request.user.is_authenticated,
        }
    )
