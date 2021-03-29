from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('quiz', TemplateView.as_view(template_name='quiz.html'), name='quiz'),
    path('profile', TemplateView.as_view(template_name='profile.html'), name='profile'),
]
