from django.urls import include, path
from django.views.generic import TemplateView
from .views import homepage


urlpatterns = [
    path('', homepage, name='home'),
    path('quiz', include('quiz.urls'), name='quiz'),
    path('forum', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('profile', TemplateView.as_view(template_name='profile.html'), name='profile'),
]
