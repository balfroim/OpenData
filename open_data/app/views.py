from django.shortcuts import render
import requests
from quiz.models import Quiz
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
    sort_criterion = "explore.popularity_score"
    result = requests.get(
        f"https://data.namur.be/api/datasets/1.0/search/?q=&rows={nb_row}&sort={sort_criterion}").json()

    featured_datasets = [
        {
            "id": dataset["datasetid"],
            "title": dataset["metas"]["title"].split(" - "),
            "theme": dataset["metas"]["theme"][0],
            "logo": THEME2LOGO[dataset["metas"]["theme"][0]]
        }
        for dataset in result["datasets"]
    ]

    today_quiz = random.choice(Quiz.objects.all())

    print(today_quiz.questions.all())
    return render(request=request,
                  template_name='home.html',
                  context={"featured_datasets": featured_datasets,
                           "today_quiz": today_quiz})
