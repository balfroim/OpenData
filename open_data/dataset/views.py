from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import TemplateDoesNotExist
from django.views.decorators.http import require_POST

from badge.registry import BadgeCache
from .models import Theme, ProxyDataset


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, 'theme.html', {'theme': theme})


def dataset_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    return render(request, 'dataset.html', {'dataset': dataset})


def popularized_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    try:
        return render(request, f'popularized/{dataset_id}.html', {'dataset': dataset})
    except TemplateDoesNotExist:
        return HttpResponse("")


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
