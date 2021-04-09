from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil")
    description = models.TextField(max_length=200)
    facebooklink = models.CharField(max_length=100, default ="")

    def __str__(self):
        return self.user.username