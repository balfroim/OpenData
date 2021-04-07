from .models import Quiz, Question, Answer
from django.contrib import admin

class QuestionInline(admin.StackedInline):
    model = Question




@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]