from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404

from .models import User
from dataset.models import Comment
from .forms import SignInForm, ProfileForm


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            user = request.user
            user.email = data['email']
            user.set_password(data['password1'])
            user.save()

            profile = user.profile
            profile.name = data['username']
            profile.is_registered = True
            profile.save()

            login(request, user)
            return redirect('my_profile')
    else:
        form = SignInForm()

    return render(request, 'sign-in.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    last_comments = Comment.objects.filter(author=user.profile).order_by('-posted_at')[:5]
    return render(request, 'profile.html', {'profile': user.profile, "last_comments": last_comments})


def my_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)
    last_comments = Comment.objects.filter(author=profile).order_by('-posted_at')[:5]
    return render(request, 'profile.html', {'profile': profile, 'form': form, "last_comments": last_comments})
