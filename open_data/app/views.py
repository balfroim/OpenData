import random

from django.shortcuts import render

from dataset.models import Theme, ProxyDataset, Question
from user.models import User
from quiz.models import Quiz


def home_page(request):
    return render(request, 'home.html', {
        'themes': Theme.get_displayed(),
        'featured_datasets': ProxyDataset.featured_datasets(),
        'last_questions': Question.objects.order_by('-content__posted_at')[:5],
        'today_quiz': random.choice(Quiz.objects.all()),
    })


def scores_page(request):
    users = User.objects.filter(profile__is_registered=True)
    users = sorted(users, key=lambda user: user.profile.score, reverse=True)
    return render(request, 'scores.html', {'users': users})
