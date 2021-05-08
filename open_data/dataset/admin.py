from django.contrib import admin
from django.utils.safestring import mark_safe

import dataset.models as models


@admin.register(models.Theme)
class ThemeAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'preview_image']

    @staticmethod
    def preview_image(obj):
        html = f'<img src="{obj.image.url}" alt="Preview image" width="128" height="128">'
        return mark_safe(html)


@admin.register(models.ProxyDataset)
class ProxyDatasetAdmin(admin.ModelAdmin):
    readonly_fields = ['modified', 'nb_downloads_total']
    search_fields = ['title']


@admin.register(models.Keyword)
class KeywordAdmin(admin.ModelAdmin):
    search_fields = ["dataset"]


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    readonly_fields = ["posted_at"]
    search_fields = ["author", "text"]


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["content", "dataset"]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ["content", "question"]


@admin.register(models.NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    autocomplete_fields = ["dataset"]


@admin.register(models.DatasetLink)
class DatasetLinkAdmin(admin.ModelAdmin):
    autocomplete_fields = ["from_dataset", "to_dataset"]
