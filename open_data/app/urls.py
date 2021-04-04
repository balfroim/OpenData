from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from .views import home, signin

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('signin/', signin, name='signin'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('quiz/', TemplateView.as_view(template_name='quiz.html'), name='quiz'),
    path('forum/', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
]
