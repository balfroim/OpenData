from django.contrib import admin
from nested_inline import admin as nested_admin
from .models import Profil, ProfilInfo

class ProfileInfoInline(nested_admin.NestedTabularInline):
    model = ProfilInfo


@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "token"]
    inlines = [
        ProfileInfoInline
    ]
