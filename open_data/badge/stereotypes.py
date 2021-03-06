from abc import ABCMeta, abstractmethod

from badge.base import Badge, BadgeAwarded


class ThresholdedBadge(Badge, metaclass=ABCMeta):
    """A badge awarded when a value reaches a certain threshold."""

    multiple = False

    @property
    @abstractmethod
    def level_thresholds(self):
        pass

    @abstractmethod
    def thresholded_value(self, user):
        pass

    def award(self, **state):
        user = state['user']
        award = None
        for lvl, badge_detail in enumerate(self.levels):
            if self.thresholded_value(user) >= self.level_thresholds[lvl]:
                award = BadgeAwarded(level=lvl + 1)
        return award


class OnceBadge(Badge, metaclass=ABCMeta):
    """A badge awarded only once when an event is fired.

    It should have only one value in its `levels` field.
    """
    multiple = False

    def award(self, **state):
        return BadgeAwarded(level=1)
