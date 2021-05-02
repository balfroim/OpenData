from django import template

from dataset.models import Theme

register = template.Library()


@register.simple_tag
def get_themes():
    return Theme.get_displayed()


@register.inclusion_tag('tags/show_datasets.html')
def show_datasets(datasets):
    return {'datasets': datasets}


@register.filter
def paginate(sequence, group_size):
    for i in range(0, len(sequence), group_size):
        yield sequence[i:i+group_size]
