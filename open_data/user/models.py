from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True)
    description = models.TextField(max_length=200, default='', blank=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
