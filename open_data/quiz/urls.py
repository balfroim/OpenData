from django.urls import path

from . import views

urlpatterns = [
    path('', views.quizzes, name='quizzes'),
    path('<int:quiz_id>/', views.quiz, name='quiz'),
]
