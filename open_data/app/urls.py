from django.urls import path
from django.views.generic import TemplateView
from django.urls import include, path

from . import views
from open_data import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('forum/', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('search/', views.search, name='search'),
    path('scores/', TemplateView.as_view(template_name='scores.html'), name='scores'),
    path('data/', TemplateView.as_view(template_name='dataset_theme.html'), name='data'),
]
