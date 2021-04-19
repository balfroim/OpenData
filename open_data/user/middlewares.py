from django.contrib.auth import login

from .models import User, Profile, generate_name


class AnonymousUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            name = generate_name()
            user = User.objects.create_user(username=name)
            profile = Profile.objects.create(user=user, name=name)
            profile.save()
            login(request, user)
        return self.get_response(request)
