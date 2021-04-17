from django.urls import path

from . import views

urlpatterns = [
    path('<dataset_id>/', views.dataset, name='dataset'),
]
