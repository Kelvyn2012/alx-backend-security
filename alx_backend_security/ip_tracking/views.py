from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit


# 5 requests per minute for anonymous users
@ratelimit(key="ip", rate="5/m", block=True)
def anonymous_sensitive_view(request):
    return JsonResponse({"message": "Anonymous access successful"})


# 10 requests per minute for authenticated users
@ratelimit(key="ip", rate="10/m", block=True)
def authenticated_sensitive_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "You must be logged in"}, status=403)
    return JsonResponse({"message": "Authenticated access successful"})
