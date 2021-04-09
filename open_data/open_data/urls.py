"""open_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from .settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('', include('app.urls')),
    path('auth/', include('user.urls')),
    path('quiz/', include('quiz.urls')),
    path('badges/', include("pinax.badges.urls", namespace="pinax_badges")),
    path('admin/', admin.site.urls),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
