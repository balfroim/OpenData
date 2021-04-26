from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from dataset.models import Content
from .forms import SignInForm, ProfileForm
from .models import User


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


@require_POST
def delete_notifications(request):
    request.user.notifications.all().delete()
    return HttpResponse()


def profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=user.profile)

    last_badges = user.badges_earned.order_by('-awarded_at')[:10]
    last_contents = Content.objects.filter(author=user.profile).order_by(
        '-posted_at')[:5]

    return render(request, 'profile.html', {
        'profile': user.profile,
        'last_badges': last_badges,
        'last_contents': last_contents,
        'form': form
    })


def my_profile(request):
    return redirect(
        reverse('profile', kwargs={"username": request.user.username})
    )
