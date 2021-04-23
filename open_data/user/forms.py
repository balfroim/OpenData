from django.forms import ModelForm
from django.forms.fields import EmailField
from django.utils.translation import gettext as _
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User, Profile


class LogInForm(AuthenticationForm):
    username = EmailField()


class SignInForm(UserCreationForm):
    email = EmailField(label=_('Email address'))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'description']
