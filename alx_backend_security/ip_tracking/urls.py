from django.urls import path
from . import views
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="IP_Tracking_API",
        default_version="v1",
        description="Public API docs",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("login-anon/", views.anonymous_sensitive_view, name="anon_login"),
    path("login-auth/", views.authenticated_sensitive_view, name="auth_login"),
    # ... your routes
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
