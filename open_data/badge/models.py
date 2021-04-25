from django.db import models
from django.utils import timezone

from user.models import User


class BadgeAward(models.Model):
    user = models.ForeignKey(User, related_name="badges_earned", on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=255)
    level = models.IntegerField()

    def __getattr__(self, attr):
        return getattr(self._badge, attr)

    def __str__(self):
        return f"{self.name!r} ({self.user.profile.name})"

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
    def image(self):
        return self._badge.levels[self.level].image

    @property
    def progress(self):
        return self._badge.progress(self.user, self.level)

    @property
    def x(self):
        return self._badge.positions[self.level][0]
    
    @property
    def y(self):
        return self._badge.positions[self.level][1]
