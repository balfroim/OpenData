from django import template

register = template.Library()


@register.inclusion_tag('quiz/quizzes.html')
def show_quizzes(quizzes):
    return {"quizzes": quizzes}


@register.inclusion_tag('quiz/quiz.html')
def show_quiz(quiz, form):
    return {"quiz": quiz, "form": form}