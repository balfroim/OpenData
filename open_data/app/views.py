import random

from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from dataset.models import ProxyDataset
from quiz.models import Quiz
from quiz.forms import QuizForm


def home(request):
    login_form = AuthenticationForm()
    signin_form = UserCreationForm()
    today_quiz = random.choice(Quiz.objects.all())
    today_quiz = QuizForm(today_quiz, request.POST)
    return render(
        request=request,
        template_name='home.html',
        context={
            "login_form": login_form,
            "signin_form": signin_form,
            "featured_datasets": ProxyDataset.objects.order_by("-stat__popularity_score")[:5],
            "today_quiz": today_quiz,
        }
    )


@require_POST
def signin(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()

    return redirect('home')


def quizzes(request):
    quizzes = [QuizForm(quiz, request.POST) for quiz in Quiz.objects.all()]
    return render(request, 'quiz.html', {'quizzes': quizzes})
