# OpenData

## C'est quoi ?

![Page d'accueil](doc/home_page.png)

**TODO**

## Comment lancer le projet sur ma machine ?

### Installer les dépendances

D'abord installer poetry en suivant les instructions de cette [page](https://python-poetry.org/docs/#installation). C'est un outil qui nous permets de gérer facilement les dépendances du projet.

Ensuite, depuis le dossier open_data, démarrer une invite de commande/shell (Sur Windows, `⊞`+`R`, puis entrer `cmd`).

Exécuter la commande [`poetry shell`](https://python-poetry.org/docs/cli/#shell) qui génére une nouvelle invite de commande utilisant un environnement virtuel python avec toutes les dépendances du projet.

Puis, [`poetry install`](https://python-poetry.org/docs/cli/#install) qui va installer les dépendances.

### Charger les datasets et les thèmes de data.namur.be

Ne pas oublier de migrer la base de données avec `manage.py migrate` et créer l'administrateur `manage.py createsuperuser`.

`manage.py load_themes` charge tout les thèmes.

`manage.py load_datasets` charge tout les datasets (attention, cela prend un peu de temps).

Si vous souhaitez simplement avoir une base de données d'aperçu, et au lieu d'utiliser les commandes précédentes, vous pouvez charger des données d'exemple en utilisant `manage.py loaddata fixtures/example.json`. Il s'agit de données factice prêtes à être employées. Plus d'informations, veuillez vous référer à [la documentation de Django](https://docs.djangoproject.com/fr/3.2/howto/initial-data/#providing-data-with-fixtures).

### Démarrer le serveur

Utilisez `manage.py runserver`, rendez-vous ensuite sur http://127.0.0.1:8000.

Cette configuration est utilisable en développement mais pas en production. Pour cela, veuillez vous renseigner dans [la documentation de Django](https://docs.djangoproject.com/fr/3.2/howto/deployment/).
