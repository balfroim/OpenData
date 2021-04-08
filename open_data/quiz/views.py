from django.shortcuts import render, get_object_or_404

from .models import Quiz
from .forms import QuizForm


def quizzes(request):
    return render(request, 'quiz/quizzes.html', {'quizzes': Quiz.objects.all()})


def quiz(request, quiz_id):
    questions = {
        int(key.replace("question_", "")): value
        for key, value in dict(request.POST).items() if key.startswith("question")
    }

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    form = QuizForm(quiz, questions, to_correct=True)

    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'form': form})
