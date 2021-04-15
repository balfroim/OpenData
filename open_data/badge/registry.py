from .base import Badge
from typing import Type


class BadgeCache:
    """
    This is responsible for storing all badges that have been registered, as
    well as providing the public API for awarding badges.

    This class should be access only by its singleton instance.
    """
    def __init__(self):
        self._event_registry = dict()
        self._registry = dict()

    @classmethod
    def instance(cls):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = cls()
            return cls._instance

    def register(self, badge: Type[Badge]):
        badge = badge()
        self._registry[badge.slug] = badge
        for event in badge.events:
            self._instance._event_registry.setdefault(event, []).append(badge)

    def possibly_award_badge(self, event, **state):
        if event in self._event_registry:
            for badge in self._event_registry[event]:
                badge.possibly_award(**state)

    def get_badge(self, slug):
        return self._registry[slug]
