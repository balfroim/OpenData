from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Theme, ProxyDataset
from badge.registry import BadgeCache


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, 'theme.html', {'theme': theme})


def dataset_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    return render(request, 'dataset.html', {'dataset': dataset})


@require_POST
def toggle_like(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    liked = dataset not in request.user.profile.liked_datasets.all()
    if liked:
        request.user.profile.liked_datasets.add(dataset)
    else:
        request.user.profile.liked_datasets.remove(dataset)

    BadgeCache.instance().possibly_award_badge('on_dataset_liked', user=request.user)

    return JsonResponse({'liked': liked, 'n_likes': dataset.liking_users.count()})
