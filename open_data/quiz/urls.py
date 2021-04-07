from django.urls import path

from . import views

app_name = "quiz"
urlpatterns = [
    # ex: /quiz/
    path('', views.quizzes, name='list'),
    # ex: /quiz/5/result
    path('<int:quiz_id>/result/', views.result, name='result'),
    # # ex: /polls/5/results/
    # path('<int:quiz_id>/results/', views.results, name='results'),
    # # ex: /polls/5/vote/
    # path('<int:quiz_id>/vote/', views.vote, name='vote'),
]