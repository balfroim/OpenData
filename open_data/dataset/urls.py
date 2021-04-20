from django.urls import path

from . import views

urlpatterns = [
    path('theme/<str:theme_id>/', views.theme_page, name='theme'),
    path('dataset/<str:dataset_id>/', views.dataset_page, name='dataset'),
    path('dataset/<str:dataset_id>/like', views.toggle_like, name='toggle_like'),
]
