from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def home(request):
    login_form = AuthenticationForm()
    signin_form = UserCreationForm()
    return render(request, 'home.html', { 'login_form': login_form, 'signin_form': signin_form })


@require_POST
def signin(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()

    return redirect('home')
