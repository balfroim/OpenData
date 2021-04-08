from django.urls import path
from django.views.generic import TemplateView

from . import views
from open_data import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('forum/', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('search/', views.search, name='search'),
]
