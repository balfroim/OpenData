from django.urls import path

from .views import badge_list

app_name = "pinax_badges"

urlpatterns = [
    path("<str:username>/", badge_list, name="badge_list"),
]
