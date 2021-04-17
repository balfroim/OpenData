from django.urls import path

from . import views

urlpatterns = [
    path('<theme_name>/', views.theme, name='theme'),
]
