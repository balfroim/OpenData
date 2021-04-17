from django import template

from dataset.models import Theme

register = template.Library()


@register.simple_tag
def get_themes():
    return Theme.get_displayed()
