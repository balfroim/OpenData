from django.urls import path
from django.views.generic import TemplateView
from .views import homepage

urlpatterns = [
    path('', homepage, name='home'),#TemplateView.as_view(template_name='home.html'), name='home'),
    path('quiz', TemplateView.as_view(template_name='quiz.html'), name='quiz'),
    path('forum', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('profile', TemplateView.as_view(template_name='profile.html'), name='profile'),
]
