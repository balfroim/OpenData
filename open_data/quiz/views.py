import itertools

from django.shortcuts import render, get_object_or_404

from .forms import QuizForm
from .models import Quiz


def check(choices, submitted_answers, to_correct):
    pass
    # corrected = []
    # values = list(itertools.chain(*questions.values()))
    # for key, value in choices:
    #     checked = str(key) in values
    #     state = ""
    #     if to_correct:
    #         is_correct = Answer.objects.get(id=key).is_correct
    #         if checked:
    #             state = "correct" if is_correct else "incorrect"
    #     corrected.append((key, value, checked, state))
    # return corrected


def quizzes(request):
    return render(request, 'quiz/quizzes.html', {'quizzes': Quiz.objects.all()})


def quiz(request, quiz_id):
    submitted_answers = tuple(
        itertools.chain.from_iterable(value for key, value in dict(request.POST).items() if key.startswith("question"))
    )

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    form = QuizForm(quiz, choices=None, to_correct=True)

    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'form': form})
