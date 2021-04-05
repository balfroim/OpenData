import random
import requests
from dataset.models import ProxyDataset
from dictor import dictor
from django.shortcuts import render
from open_data.settings import API_URL
from quiz.forms import QuizForm
from quiz.models import Quiz


def homepage(request):
    today_quiz = random.choice(Quiz.objects.all())
    today_quiz = QuizForm(today_quiz, request.POST)
    return render(request=request,
                  template_name='home.html',
                  context={"featured_datasets": ProxyDataset.objects.order_by("-stat__popularity_score").all()[:5],
                           "today_quiz": today_quiz})


def quizzes(request):
    quizzes = [QuizForm(quiz, request.POST) for quiz in Quiz.objects.all()]
    return render(request, 'quiz.html', {'quizzes': quizzes})
