from django.dispatch import Signal
from django.dispatch import receiver
from notifications.signals import notify

badge_awarded_signal = Signal(providing_args=["badge"])


@receiver(badge_awarded_signal)
def badge_awarded(**kwargs):
    badge_award = kwargs["badge_award"]
    notify.send(badge_award.user, recipient=badge_award.user,
                verb=f'Vous avez gagné le badge : {badge_award.name}',
                image=badge_award.image)
