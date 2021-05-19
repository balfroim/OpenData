# OpenData

## C'est quoi ?

**TODO**

## Comment lancer le projet sur ma machine ?

### Installer les dépendances

D'abord installer poetry en suivant les instructions de cette [page](https://python-poetry.org/docs/#installation). C'est un outil qui nous permets de gérer facilement les dépendances du projet.

Ensuite, depuis le dossier open_data, démarrer une invite de commande/shell (Sur Windows, `⊞`+`R`, puis entrer `cmd`).

Exécuter la commande [`poetry shell`](https://python-poetry.org/docs/cli/#shell) qui génére une nouvelle invite de commande utilisant un environnement virtuel python avec toutes les dépendances du projet.

Puis, [`poetry install`](https://python-poetry.org/docs/cli/#install) qui va installer les dépendances.


### Charger les datasets et les thèmes de data.namur

`manage.py load_themes` charge tout les thèmes
`manage.py load_datasets` charge tout les datasets (prends un peu de temps attention !!)

### Démarrer le serveur

(Ne pas oublier de migrer la base de données avec `manage.py migrate` et créer l'administrateur `manage.py createsuperuser`)

`manage.py runserver` puis se rendre sur http://127.0.0.1:8000
