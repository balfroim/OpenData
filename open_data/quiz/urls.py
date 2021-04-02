from django.urls import path

from . import views

app_name = "quiz"
urlpatterns = [
    # # ex: /quiz/
    path('', views.index, name='index'),
    # ex: /quiz/5/
    # path('<int:quiz_id>/', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # path('<int:quiz_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:quiz_id>/vote/', views.vote, name='vote'),
]