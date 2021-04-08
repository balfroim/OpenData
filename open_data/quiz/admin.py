from django.contrib import admin
from nested_inline import admin as nested_admin

from .models import Quiz, Question, Answer, QuizSubmission


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 1


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [
        AnswerInline
    ]
    extra = 1


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    autocomplete_fields = ["dataset"]
    readonly_fields = ["created_at"]
    inlines = [
        QuestionInline
    ]


@admin.register(QuizSubmission)
class QuizSubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ["taken_at", "good_answers_count"]
