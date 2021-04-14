import random

from django.contrib.auth import login
from django.contrib.auth.models import User

from profil.models import Profil


class AnonymousUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            username = f"Datasorus#{random.randrange(10000)}"
            user = User.objects.create_user(username=username)
            profile = Profil.objects.create(user=user)
            profile.save()
            login(request, user)
        response = self.get_response(request)
        return response
