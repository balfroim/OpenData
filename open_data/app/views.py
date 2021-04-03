from django.shortcuts import render
import requests
from quiz.models import Quiz
from quiz.forms import QuizForm
import random

THEME2LOGO = {
    'Santé': 'doctors',
    'Population, Statistiques': 'outline_group',
    'Aménagement du territoire, Urbanisme, Bâtiments, Equipements, Logement': 'townplanning',
    'Administration, Gouvernement, Finances publiques, Citoyenneté': 'administration',
    'Transports, Déplacements': '',
    'Energie': '',
    'Sport, Loisirs': '',
    'Culture, Patrimoine': '',
    'Environnement': '',
    'Interne': '',
    'Education, Formation, Recherche, Enseignement': '',
    'Economie, Business, PME, Développement économique, Emploi': '',
    'Closed Data, Accès restreint': '',
}


# Create your views here.
def homepage(request):
    nb_row = 5
    sort_criterion = "explore.popularity_score desc"
    url = f"https://data.namur.be/api/v2/catalog/datasets?order_by={sort_criterion}&limit={nb_row}" \
        f"&timezone=UTC&include_app_metas=true"
    result = requests.get(url).json()
    featured_datasets = [
        {
            "id": dataset["dataset"]["dataset_id"],
            "title": dataset["dataset"]["metas"]["default"]["title"].split(" - "),
            "themes": dataset["dataset"]["metas"]["default"]["theme"],
            "logo": THEME2LOGO[dataset["dataset"]["metas"]["default"]["theme"][0]]
        }
        for dataset in result["datasets"]
    ]

    today_quiz = random.choice(Quiz.objects.all())
    if request.method == 'POST':
        today_quiz = QuizForm(today_quiz, request.POST)
    else:
        today_quiz = QuizForm(today_quiz)

    return render(request=request,
                  template_name='home.html',
                  context={"featured_datasets": featured_datasets,
                           "today_quiz": today_quiz})


def quizzes(request):
    return render(request, 'quiz.html', {'quizzes': Quiz.objects.all()})
