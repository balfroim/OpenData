import random

from django import template

from quiz.forms import QuizForm
from quiz.models import QuizSubmission

register = template.Library()


@register.inclusion_tag('quiz/quiz.html', takes_context=True)
def show_quiz(context, quiz):
    user = context['request'].user
    try:
        submission = QuizSubmission.objects.get(quiz=quiz, user=user)
        return {
            'quiz': quiz,
            'form': QuizForm(quiz, submission.choices),
            'submittable': False
        }
    except QuizSubmission.DoesNotExist:
        return {
            'quiz': quiz,
            'form': QuizForm(quiz),
            'submittable': True
        }


@register.inclusion_tag('quiz/quizzes.html')
def show_quizzes(quizzes):
    return {'quizzes': quizzes.all()}


@register.filter
def to_list(i):
    """Cast any iterable i into a list"""
    return list(i)


@register.filter
def shuffle(l: list):
    """Shuffle randomly a list"""
    return random.sample(l, len(l))
