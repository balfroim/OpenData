from django.apps import AppConfig

class BadgeConfig(AppConfig):
    name = 'badge'

    def ready(self):
        from badge.badges.quiz import QuizBadge
        from .registry import badges
        badges.register(QuizBadge)
        from .signals.badge_awarded import badge_awarded


