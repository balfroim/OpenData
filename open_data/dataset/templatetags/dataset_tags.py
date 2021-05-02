from django import template

from dataset.models import Theme

register = template.Library()


@register.simple_tag
def get_themes():
    return Theme.get_displayed()


@register.filter
def paginate(sequence, group_size):
    for i in range(0, len(sequence), group_size):
        yield sequence[i:i+group_size]
