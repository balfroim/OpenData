from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from profil.models import Profil


def sign_in(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profil.objects.create(user=user)
            profile.save()
            login(request, user)
            return redirect('profil', username=user.username)
    else:
        form = UserCreationForm()

    return render(request, 'sign-in.html', {'form': form})
