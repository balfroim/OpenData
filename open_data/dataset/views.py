from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import ProxyDataset


def main(request, dataset_id):
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
