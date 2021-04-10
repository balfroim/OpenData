from dataset.models import Theme, ProxyDataset, ProxyDatasetStat
from django.contrib import admin
from django.utils.safestring import mark_safe


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    readonly_fields = ["name", "slug", "preview_image"]

    def preview_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width=128px height=128px/>')

@admin.register(ProxyDataset)
class ProxyDatasetAdmin(admin.ModelAdmin):
    readonly_fields = ["modified"]


    search_fields = ["title"]