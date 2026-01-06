from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views


# Swagger/OpenAPI Schema Configuration
schema_view = get_schema_view(
    openapi.Info(
        title="IP Tracking API",
        default_version="v1",
        description="API for tracking IP addresses with rate limiting and authentication",
        contact=openapi.Contact(email="your-email@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = "ip_tracking"

urlpatterns = [
    # API Documentation
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="api-docs",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="api-redoc",
    ),
    path(
        "swagger.json",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    # API Endpoints
    path("login/anonymous/", views.anonymous_sensitive_view, name="login-anonymous"),
    path(
        "login/authenticated/",
        views.authenticated_sensitive_view,
        name="login-authenticated",
    ),
    path("user/info/", views.user_info_view, name="user-info"),
]
