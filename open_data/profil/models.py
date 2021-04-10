import uuid
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profil", null=True, blank=True)
    token = models.CharField(max_length=36, null=True, blank=True)
    created_at = models.DateTimeField(help_text="La date de création du profil.")

    def save(self, *args, **kwargs):
        if not self.id:
            self.token = str(uuid.uuid4())
            self.created_at = timezone.now()
        return super(Profil, self).save(*args, **kwargs)

    def __str__(self):
        if self.user:
            return self.user.username
        return f"Datanonymous#{self.id}"


class ProfilInfo(models.Model):
    profil = models.OneToOneField(Profil, on_delete=models.CASCADE, related_name="infos")
    description = models.TextField(max_length=200, default='', blank=True)
