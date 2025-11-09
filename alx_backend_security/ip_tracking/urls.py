from django.urls import path
from ip_tracking import views

urlpatterns = [
    path('login-anon/', views.anonymous_sensitive_view, name='anon_login'),
    path('login-auth/', views.authenticated_sensitive_view, name='auth_login'),
]
