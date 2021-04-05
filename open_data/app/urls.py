from django.urls import include, path
from django.views.generic import TemplateView
from . import views
from open_data.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static


urlpatterns = [
    path('', views.homepage, name='home'),
    path('quiz/', include('quiz.urls'), name='quiz'),
    path('quizzes', views.quizzes, name='quizzes'),
    path('forum', TemplateView.as_view(template_name='forum.html'), name='forum'),
    path('profile', TemplateView.as_view(template_name='profile.html'), name='profile'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
