from django import template
import random

register = template.Library()


@register.inclusion_tag('quiz/quizzes.html')
def show_quizzes(quizzes):
    return {"quizzes": quizzes}


@register.inclusion_tag('quiz/quiz.html')
def show_quiz(quiz):
    return {"quiz": quiz}


@register.filter
def to_list(i):
    """Cast any iterable i into a list"""
    return list(i)


@register.filter
def shuffle(l: list):
    """Shuffle randomly a list l"""
    return random.sample(l, len(l))
