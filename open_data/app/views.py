import random

from django.db.models import Count
from django.shortcuts import render

from badge.registry import BadgeCache
from dataset.models import Theme, ProxyDataset, Question
from quiz.models import Quiz
from user.models import User


def home_page(request):
    all_datasets = ProxyDataset.objects.annotate(
        nb_likes=Count('liking_users__id'),
        nb_questions=Count('questions__id')
    )
    featured_datasets = [
        {
            "reason": 'Jeu de données d\'actualité',
            "dataset": all_datasets.order_by('-articles__date').first()
        }
    ]
    featured_datasets = extract_featured_datasets(
        "jeu de données le populaire.",
        2,
        all_datasets.order_by('-popularity_score'),
        featured_datasets
    )
    featured_datasets = extract_featured_datasets(
        "jeu de données le plus téléchargé.",
        1,
        sorted(all_datasets, key=lambda dataset: dataset.nb_downloads_total, reverse=True),
        featured_datasets
    )
    featured_datasets = extract_featured_datasets(
        "jeu de données le plus aimé.",
        1,
        all_datasets.order_by('-nb_likes'),
        featured_datasets
    )
    featured_datasets = extract_featured_datasets(
        "jeu de données avec le plus de questions.",
        1,
        all_datasets.order_by('-nb_questions'),
        featured_datasets
    )
    return render(request, 'home.html', {
        'themes': Theme.get_displayed(),
        'featured_datasets': featured_datasets,
        'last_questions': Question.objects.order_by('-content__posted_at')[:5],
        'today_quiz': random.choice(Quiz.objects.all()),
    })


def extract_featured_datasets(reason, nb_to_take, datasets, featured_datasets):
    max_len = len(featured_datasets) + nb_to_take
    for i, dataset in enumerate(datasets):
        if dataset not in [d["dataset"] for d in featured_datasets]:
            featured_datasets.append({
                "index": i + 1,
                "reason": reason,
                "dataset": dataset
            })
            if len(featured_datasets) >= max_len:
                break
    return featured_datasets


def scores_page(request):
    users = User.objects.filter(profile__is_registered=True)
    users = sorted(users, key=lambda user: user.profile.score, reverse=True)
    BadgeCache.instance().possibly_award_badge("top_1", user=users[0])
    return render(request, 'scores.html', {'users': users})
