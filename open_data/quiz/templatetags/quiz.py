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
def shuffle(arg):
    list_arg = list(arg)
    return random.sample(list_arg, len(list_arg))
