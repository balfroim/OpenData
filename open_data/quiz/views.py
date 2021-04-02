from django.shortcuts import render

from .models import Quiz


def index(request):
    latest_quizzes = Quiz.objects.order_by('-created_at')[:5]
    return render(request, 'quiz/index.html', {'latest_quizzes': latest_quizzes})
# def quiz(request, question_id):
#

#
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)