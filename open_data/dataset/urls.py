from django.urls import path

from . import views

urlpatterns = [
    path('<str:dataset_id>/', views.main, name='dataset'),
    path('<str:dataset_id>/like', views.toggle_like, name='toggle_like'),
]
