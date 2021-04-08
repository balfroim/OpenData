from .models import Quiz, Question, Answer
from django.contrib import admin
from nested_inline import admin as nested_admin

class AnswerInline (nested_admin.NestedTabularInline):
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
    inlines = [
        QuestionInline
    ]