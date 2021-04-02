from django.shortcuts import render

from .models import Quiz


def quizzes(request):
    return render(request, 'quiz.html', {'quizzes': Quiz.objects.all()})
# def quiz(request, question_id):
#

#
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)