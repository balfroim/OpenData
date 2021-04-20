import random

from django.shortcuts import render

from dataset.models import Theme, ProxyDataset
from quiz.forms import QuizForm
from quiz.models import Quiz


def home(request):
    return render(request, 'home.html', {
        'themes': Theme.get_displayed(),
        'featured_datasets': ProxyDataset.objects.order_by('-popularity_score')[:5],
        'today_quiz': random.choice(Quiz.objects.all()),
    })


def quizzes(request):
    quizzes = [QuizForm(quiz, request.POST) for quiz in Quiz.objects.all()]
    return render(request, 'quiz.html', {'quizzes': quizzes})


def search(request):
    return render(request, 'search.html')
