from pinax.badges.signals import badge_awarded
from django.dispatch import receiver

@receiver(badge_awarded)
def badge_awarded(**kwargs):
    print("You won a badge : " + kwargs["badge_award"].name )