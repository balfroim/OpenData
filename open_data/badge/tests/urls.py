from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("badge.urls", namespace="pinax_badges")),
]
