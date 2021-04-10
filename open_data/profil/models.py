from django.db import models
from django.contrib.auth.models import User

class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil", null=True)
    description = models.TextField(max_length=200)

    def __str__(self):
        return self.user.username

