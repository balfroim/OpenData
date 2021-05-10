from django.urls import path

from . import views

urlpatterns = [
    path('theme/<int:theme_id>/', views.theme_page, name='theme'),
    path('theme/<int:theme_id>/subscribe', views.toggle_subscription, name='toggle_subscription'),
    path('dataset/<str:dataset_id>/', views.dataset_page, name='dataset'),
    path('dataset/<str:dataset_id>/like', views.toggle_like, name='toggle_like'),
    path('dataset/<str:dataset_id>/download', views.download_dataset, name='download_dataset'),
    path('dataset/<str:dataset_id>/popularized', views.popularized_page, name='popularized'),
    path('dataset/<str:dataset_id>/questions', views.questions_page, name="questions"),
    path('question/add', views.add_question, name='add-question'),
    path('question/<int:question_id>', views.question_page, name='question'),
    path('question/<int:question_id>/rmv', views.rmv_question, name='rmv-question'),
    path('question/<int:question_id>/answer/add', views.add_answer, name='add-answer'),
    path('answer/<int:answer_id>/rmv', views.rmv_answer, name='rmv-answer'),
    path('search/', views.search_page, name='search'),
]
