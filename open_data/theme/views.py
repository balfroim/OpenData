from django.shortcuts import render, get_object_or_404

from ..dataset.models import ProxyDataset, Theme

def theme(request, theme_name):
    theme = get_object_or_404(Theme, id=theme_name)
    return render(request, 'theme.html', {'theme': theme})


def dataset(request, dataset_id):
    dataset = get_object_or_404(ProxyDataset, id=dataset_id)
    return render(request, 'dataset.html', {'dataset': dataset})
