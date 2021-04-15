from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('forum/', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('search/', views.search, name='search'),
    path('scores/', TemplateView.as_view(template_name='scores.html'), name='scores'),
    path('data/', TemplateView.as_view(template_name='data.html'), name='data'),
]
