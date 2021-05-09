from django import template

from dataset.models import Theme, ProxyDataset

register = template.Library()


@register.simple_tag
def get_themes():
    return Theme.get_displayed()


@register.inclusion_tag('tags/show_datasets.html')
def show_datasets(datasets, tab_id=0):
    return {
        'datasets': datasets,
        'tab_prefix': f'page-{tab_id}-',
    }


@register.filter
def paginate(sequence, group_size):
    for i in range(0, len(sequence), group_size):
        yield sequence[i:i+group_size]
