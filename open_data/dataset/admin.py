from dataset.models import Theme
from django.contrib import admin
from django.utils.safestring import mark_safe


@admin.register(Theme)
class HeroAdmin(admin.ModelAdmin):
    readonly_fields = ["name", "slug", "preview_image"]

    def preview_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width=128px height=128px/>')