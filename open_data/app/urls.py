from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('forum/', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('scoreboard/', views.scoreboard, name='scores'),
    path('data/', TemplateView.as_view(template_name='dataset_theme.html'), name='data'),
]
