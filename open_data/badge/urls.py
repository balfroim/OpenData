from django.conf.urls import url

from .views import badge_list

app_name = "pinax_badges"

urlpatterns = [
    url(r"^$", badge_list, name="badge_list"),
]
