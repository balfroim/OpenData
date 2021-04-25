from badge.base import Badge, BadgeAwarded

from abc import ABCMeta, abstractmethod


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
        user = state["user"]

        for lvl, badge_detail in enumerate(self.levels):
            if self.thresholded_value(user) >= self.level_thresholds[lvl]:
                award = BadgeAwarded(level=lvl+1)
                if award:
                    user.profile.add_score(badge_detail.score)
                    print(f"{user.profile.score} (+{badge_detail.score})")
                    return award

