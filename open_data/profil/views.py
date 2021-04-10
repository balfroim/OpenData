from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User


def index(request,username):
    user = get_object_or_404(User, username=username)
    return render(request, 'profil/profile.html', {"targetuser": user})
