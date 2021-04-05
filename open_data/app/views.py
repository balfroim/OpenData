import random
import requests
from dataset.models import Theme
from dictor import dictor
from django.shortcuts import render
from open_data.settings import API_URL
from quiz.forms import QuizForm
from quiz.models import Quiz


def homepage(request):
    nb_row = 5
    sort_criterion = "explore.popularity_score desc"
    url = f"{API_URL}catalog/datasets?order_by={sort_criterion}&limit={nb_row}" \
        f"&timezone=UTC&include_app_metas=true"
    result = requests.get(url).json()
    featured_datasets = [
        {
            "id": dataset["dataset"]["dataset_id"],
            "title": dataset["dataset"]["metas"]["default"]["title"].split(" - "),
            # "themes": dataset["dataset"]["metas"]["default"]["theme"],
            "theme": Theme.objects.get(name=dataset["dataset"]["metas"]["default"]["theme"][0])
        }
        for dataset in result["datasets"]
    ]

    print(dictor(featured_datasets, "logo"))

    today_quiz = random.choice(Quiz.objects.all())
    today_quiz = QuizForm(today_quiz, request.POST)
    # print(today_quiz.correct())
    # load_themes()
    # load_datasets()
    return render(request=request,
                  template_name='home.html',
                  context={"featured_datasets": featured_datasets,
                           "today_quiz": today_quiz})


def quizzes(request):
    quizzes = [QuizForm(quiz, request.POST) for quiz in Quiz.objects.all()]
    return render(request, 'quiz.html', {'quizzes': quizzes})
