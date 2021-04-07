import random

from django.shortcuts import render, redirect

from dataset.models import ProxyDataset
from quiz.models import Quiz
from quiz.forms import QuizForm


def home(request):
    today_quiz = random.choice(Quiz.objects.all())
    today_quiz = QuizForm(today_quiz, request.POST)
    return render(request, 'home.html', {
        'featured_datasets': ProxyDataset.objects.order_by('-stat__popularity_score')[:5],
        'today_quiz': today_quiz,
    })


def quizzes(request):
    quizzes = [QuizForm(quiz, request.POST) for quiz in Quiz.objects.all()]
    return render(request, 'quiz.html', {'quizzes': quizzes})


def search(request):
    return render(request, 'search.html')
