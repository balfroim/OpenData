from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('forum/', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('scores/', TemplateView.as_view(template_name='scores.html'), name='scores'),
    path('theme/<str:theme_name>', TemplateView.as_view(template_name='theme.html'), name='theme'),
]
