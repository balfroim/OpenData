from django import template
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

register = template.Library()


@register.inclusion_tag('log-in-form.html')
def log_in_form(form=AuthenticationForm()):
    return {'form': form}


@register.inclusion_tag('sign-in-form.html')
def sign_in_form(form=UserCreationForm()):
    return {'form': form}
