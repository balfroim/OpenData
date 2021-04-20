from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Theme, ProxyDataset


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'preview_image']

    def preview_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" alt="Preview image" width="128" height="128">')


@admin.register(ProxyDataset)
class ProxyDatasetAdmin(admin.ModelAdmin):
    readonly_fields = ['modified']
    search_fields = ['title']
