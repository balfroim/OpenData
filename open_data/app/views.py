import random

from django.shortcuts import render

from dataset.models import Theme, ProxyDataset, Question
from user.models import Profile
from quiz.models import Quiz


def home_page(request):
    return render(request, 'home.html', {
        'themes': Theme.get_displayed(),
        'featured_datasets': ProxyDataset.objects.order_by('-popularity_score')[:5],
        'last_questions': Question.objects.order_by('-posted_at')[:5],
        'today_quiz': random.choice(Quiz.objects.all()),
    })


def scores_page(request):
    profiles = Profile.objects.filter(is_registered=True)
    profiles = sorted(profiles, key=lambda profile: profile.score, reverse=True)
    return render(request, 'scores.html', {'profiles': profiles})
