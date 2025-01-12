from django.contrib.auth import logout
from django.http import JsonResponse


def register(request):
    pass


def login_view(request):
    pass


def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logged out successfully'})
