from django.shortcuts import render, get_object_or_404

from .models import ProxyDataset


def dataset(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    return render(request, 'dataset.html', {'dataset': dataset})
