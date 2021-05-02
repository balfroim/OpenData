from django.contrib.auth import login

from .models import User


class AnonymousUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            user = User.objects.create_user()
            login(request, user)
        return self.get_response(request)
