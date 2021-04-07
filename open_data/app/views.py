from dataset.models import ProxyDataset
from django.shortcuts import render
from quiz.forms import QuizForm
from quiz.models import Quiz


def home(request):
    today_quiz = Quiz.objects.all()[0]
    # if request.POST:
    #     questions = {int(key.replace("question_", "")): value
    #                  for key, value in dict(request.POST).items() if
    #                  key.startswith("question")}
    #     today_quiz = QuizForm(today_quiz, questions)
    # else:
    today_quiz = QuizForm(today_quiz)

    return render(request, 'home.html', {
        'featured_datasets': ProxyDataset.objects.order_by('-stat__popularity_score')[:5],
        'today_quiz': today_quiz,
    })


def quizzes(request):
    quizzes = [QuizForm(quiz, request.POST) for quiz in Quiz.objects.all()]
    return render(request, 'quiz.html', {'quizzes': quizzes})


def search(request):
    return render(request, 'search.html')
