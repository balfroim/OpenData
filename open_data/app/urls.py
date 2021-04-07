from django.urls import include, path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

from . import views
from open_data import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/', include('quiz.urls'), name='quiz'),
    path('quizzes/', views.quizzes, name='quizzes'),
    path('forum/', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('profile/', TemplateView.as_view(template_name='profile.html'), name='profile'),
    path('search/', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
