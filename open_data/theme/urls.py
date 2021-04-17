from django.urls import path

from . import views

urlpatterns = [
    path('<str:theme_name>/', views.theme, name='theme'),
]
