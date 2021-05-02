import json
from typing import Type

from open_data.settings import BADGES_PATH

from .base import Badge


class BadgeCache:
    """
    This is responsible for storing all badges that have been registered, as
    well as providing the public API for awarding badges.

    This class should be access only by its singleton instance.
    """

    def __init__(self):
        self._event_registry = dict()
        self._registry = dict()
        # Get badges' positions from json
        try:
            with open(BADGES_PATH, 'r') as file:
                self.badges_positions = json.load(file)
        except FileNotFoundError:
            self.badges_positions = {}

    @classmethod
    def instance(cls):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = cls()
            return cls._instance

    def register(self, badge_cls: Type[Badge]):
        badge_cls.positions = []
        for i, _ in enumerate(badge_cls.levels):
            name = f'{badge_cls.slug}:{i}'
            position = self.badges_positions.get(name, {'x': 1, 'y': 1})
            badge_cls.positions.append([position['x'], position['y']])
        badge = badge_cls()
        self._registry[badge.slug] = badge
        for event in badge.events:
            self._instance._event_registry.setdefault(event, []).append(badge)

    def possibly_award_badge(self, event, **state):
        if event in self._event_registry:
            for badge in self._event_registry[event]:
                badge.possibly_award(**state)

    def get_badge(self, slug):
        return self._registry[slug]

    def all(self):
        return tuple(self._registry)
