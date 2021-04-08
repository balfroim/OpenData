from django.urls import path

from . import views

urlpatterns = [
    path('', views.quizzes, name='list'),
    path('<int:quiz_id>/', views.result, name='result'),
]
