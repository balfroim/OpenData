import random

from django.db.models import Count
from django.shortcuts import render

from dataset.models import Theme, ProxyDataset, Question
from quiz.models import Quiz
from user.models import User


def home_page(request):
    all_datasets = ProxyDataset.objects.annotate(
        nb_likes=Count('liking_users__id'),
        nb_questions=Count('questions__id')
    )
    already_matched_ids = set()
    featured_datasets = set()
    for i, dataset in enumerate(all_datasets.order_by('-popularity_score')):
        if dataset.id not in already_matched_ids:
            featured_datasets.add((dataset, i+1, "jeu de données le populaire."))
            already_matched_ids.add(dataset.id)
            if len(already_matched_ids) >= 3:
                break
    for i, dataset in enumerate(all_datasets.order_by('-nb_likes')):
        if dataset.id not in already_matched_ids:
            featured_datasets.add((dataset, i+1, "jeu de données le plus aimé."))
            already_matched_ids.add(dataset.id)
            if len(already_matched_ids) >= 4:
                break
    for i, dataset in enumerate(all_datasets.order_by('-nb_questions')):
        if dataset.id not in already_matched_ids:
            featured_datasets.add((dataset, i+1, "jeu de données avec le plus de questions."))
            already_matched_ids.add(dataset.id)
            if len(already_matched_ids) >= 5:
                break
    return render(request, 'home.html', {
        'themes': Theme.get_displayed(),
        'featured_datasets': featured_datasets,
        'last_questions': Question.objects.order_by('-content__posted_at')[:5],
        'today_quiz': random.choice(Quiz.objects.all()),
    })


def scores_page(request):
    users = User.objects.filter(profile__is_registered=True)
    users = sorted(users, key=lambda user: user.profile.score, reverse=True)
    return render(request, 'scores.html', {'users': users})
