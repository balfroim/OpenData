from django import template

from dataset.models import Theme

register = template.Library()


@register.simple_tag
def get_themes():
    return Theme.get_displayed()


@register.inclusion_tag('modals/comments.html')
def show_comments(dataset, user):
    return {"dataset": dataset, "is_registered": user.profile.is_registered}
