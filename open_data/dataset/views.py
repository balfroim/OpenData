from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Theme, ProxyDataset


def theme_page(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    return render(request, 'theme.html', {'theme': theme})


def dataset_page(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    return render(request, 'dataset.html', {'dataset': dataset})


@require_POST
def toggle_like(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    if dataset in request.user.profile.liked_datasets.all():
        request.user.profile.liked_datasets.remove(dataset)
    else:
        request.user.profile.liked_datasets.add(dataset)

    return redirect('dataset', dataset_id=dataset.id)
