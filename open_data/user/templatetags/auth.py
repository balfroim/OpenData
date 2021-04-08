from django import template
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

register = template.Library()


@register.inclusion_tag('log-in-form.html', takes_context=True)
def log_in_form(context, form=AuthenticationForm()):
    request = context['request']
    next = form.data.get('next', request.path)
    return {'form': form, 'next': next}


@register.inclusion_tag('sign-in-form.html', takes_context=True)
def sign_in_form(context, form=UserCreationForm()):
    request = context['request']
    next = form.data.get('next', request.path)
    return {'form': form, 'next': next}
