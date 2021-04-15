from django.apps import AppConfig


class BadgeConfig(AppConfig):
    name = 'badge'

    def ready(self):
        from badge.badges.quiz import QuizBadge
        from badge.registry import BadgeCache
        BadgeCache.instance().register(QuizBadge)
        from badge.signals import badge_awarded


