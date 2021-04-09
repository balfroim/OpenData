from .models import Profil
from django.contrib import admin
from nested_inline import admin as nested_admin

@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    pass