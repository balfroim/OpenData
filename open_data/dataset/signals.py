from django.dispatch import receiver
from django.db.models.signals import post_delete
from dataset.models import Question, Answer


@receiver(post_delete, sender=Question)
def post_delete_question(sender, instance, *args, **kwargs):
    if instance.content:
        instance.content.delete()


@receiver(post_delete, sender=Answer)
def post_delete_answer(sender, instance, *args, **kwargs):
    if instance.content:
        instance.content.delete()
