import secrets

from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser


def generate_name():
    return f'user{secrets.randbelow(1000000)}'


class User(AbstractUser):
    # https://stackoverflow.com/a/43209322

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS

    email = models.EmailField(_('Email address'), unique=True, null=True, default=None)  # changes email to unique and blank to false

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = None
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True)
    name = models.CharField(max_length=24, default=generate_name)
    description = models.TextField(max_length=200, default='', blank=True)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.name
