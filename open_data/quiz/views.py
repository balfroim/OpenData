from django.shortcuts import render, get_object_or_404

from .models import Quiz


def quizzes(request):
    return render(request, 'quiz/quizzes.html', {'quizzes': Quiz.objects.all()})


def quiz(request, quiz_id):
    return render(request, 'quiz/quiz.html', {'quiz': get_object_or_404(Quiz, pk=quiz_id)})