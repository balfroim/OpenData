from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('scores/', views.scores_page, name='scores'),
]
