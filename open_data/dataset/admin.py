from django.contrib import admin
from django.utils.safestring import mark_safe

from dataset.models import Theme, ProxyDataset, Keyword, Question, Content, Answer


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    readonly_fields = ['name', 'preview_image']

    def preview_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" alt="Preview image" width="128" height="128">')


@admin.register(ProxyDataset)
class ProxyDatasetAdmin(admin.ModelAdmin):
    readonly_fields = ['modified']
    search_fields = ['title']


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    search_fields = ["dataset"]


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    readonly_fields = ["posted_at"]
    search_fields = ["author", "text"]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ["content", "dataset"]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    search_fields = ["content", "question"]
