from django import template

register = template.Library()


@register.inclusion_tag('profil/profiles.html')
def show_profiles(profiles):
    return {"profiles": profiles}


