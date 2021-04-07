from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path('log-in/', LoginView.as_view(template_name="log-in.html"), name='log_in'),
    path('log-out/', LogoutView.as_view(), name='log_out'),
    path('sign-in/', views.sign_in, name='sign_in'),
]
