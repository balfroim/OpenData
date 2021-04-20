from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .forms import LogInForm

urlpatterns = [
    path('log-in/', LoginView.as_view(template_name='log-in.html', authentication_form=LogInForm), name='log_in'),
    path('log-out/', LogoutView.as_view(), name='log_out'),
    path('sign-in/', views.sign_in, name='sign_in'),
    path('me/', views.my_profile, name='my_profile'),
    path('<str:username>/', views.profile, name='profile'),
]
