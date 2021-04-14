from django.dispatch import receiver
from notifications.signals import notify

from django.dispatch import Signal

badge_awarded = Signal(providing_args=["badge"])

@receiver(badge_awarded)
def badge_awarded(**kwargs):
    badge_award = kwargs["badge_award"]
    notify.send(badge_award.user, recipient=badge_award.user, verb=f'Vous avez gagné le badge : {badge_award.name}')
