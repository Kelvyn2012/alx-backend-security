from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def home(request):
    return JsonResponse({"message": "Welcome to ALX Backend Security"})


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("ip_tracking/", include("ip_tracking.urls")),
]
