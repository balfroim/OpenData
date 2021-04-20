from django.db import models
from django.utils import timezone
from notifications.base.models import AbstractNotification

from user.models import User


class BadgeAward(models.Model):
    user = models.ForeignKey(User, related_name="badges_earned", on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=255)
    level = models.IntegerField()

    def __getattr__(self, attr):
        return getattr(self._badge, attr)

    def __str__(self):
        return f"\"{self.name}\" [{self.user.profile.name}"

    @property
    def badge(self):
        return self

    @property
    def _badge(self):
        from badge.registry import BadgeCache
        return BadgeCache.instance().get_badge(self.slug)

    @property
    def name(self):
        return self._badge.levels[self.level].name

    @property
    def description(self):
        return self._badge.levels[self.level].description

    @property
    def progress(self):
        return self._badge.progress(self.user, self.level)

    @property
    def image(self):
        try:
            images = self._badge.images
        except AttributeError:
            return "default.png"
        if isinstance(images, str):
            return images
        return images[self.level]


class BadgeNotification(AbstractNotification):
    badge = models.OneToOneField(BadgeAward, related_name="notification", on_delete=models.CASCADE)

    class Meta(AbstractNotification.Meta):
        abstract = False
