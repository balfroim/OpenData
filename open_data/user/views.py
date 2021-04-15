from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404


def sign_in(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = request.user
            user.set_password(new_user.password)
            user.username = new_user.username
            user.email = new_user.email
            user.save()
            return redirect('profile', username=user.username)
    else:
        form = UserCreationForm()

    return render(request, 'sign-in.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {"profile_user": user})
