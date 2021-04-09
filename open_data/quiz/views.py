import itertools

from django.shortcuts import render, get_object_or_404
from pinax.badges.registry import badges

from .forms import QuizForm
from .models import Quiz, Answer, QuizSubmission


def check(quiz, submitted_answers):
    good_answers_count = 0
    choices = []
    for question in quiz.questions.all():
        question_choices = []
        for id, text in question.answers.values_list('id', 'text'):
            checked = str(id) in submitted_answers
            is_correct = Answer.objects.get(id=id).is_correct
            if is_correct and checked:
                state = "correct"
                good_answers_count += 1
            elif is_correct and not checked:
                state = "missing"
                checked = True
            else:
                state = "incorrect"
            question_choices.append((id, text, checked, state))
        choices.append(tuple(question_choices))
    return tuple(choices), good_answers_count


def quizzes(request):
    return render(request, 'quiz/quizzes.html', {'quizzes': Quiz.objects.all()})


def quiz(request, quiz_id):
    submitted_answers = tuple(
        itertools.chain.from_iterable(
            value for key, value in dict(request.POST).items() if key.startswith("question")
        )
    )

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    choices, good_answers_count = check(quiz, submitted_answers)
    submission = QuizSubmission(user=request.user, quiz=quiz, good_answers_count=good_answers_count, choices=choices)
    submission.save()
    badges.possibly_award_badge("quiz_submit", user=request.user)
    form = QuizForm(quiz, choices)

    return render(request, 'quiz/quiz.html', {'quiz': quiz, 'form': form})
