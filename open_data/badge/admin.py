from django.contrib import admin

from badge.models import BadgeAward


@admin.register(BadgeAward)
class BadgeAwardAdmin(admin.ModelAdmin):
    pass
