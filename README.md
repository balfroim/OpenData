# OpenData

## C'est quoi ?

**TODO**

## Comment lancer le projet sur ma machine ?

### Cloner le repositery

[Tutoriel officiel de git (en anglais)][https://docs.github.com/en/github/getting-started-with-github/about-remote-repositories]

### Installer les dépendances

D'abord installer poetry en suivant les instructions de cette [page](https://python-poetry.org/docs/#installation). C'est un outil qui nous permets de gérer facilement les dépendances du projet.

Ensuite, depuis le dossier open_data, démarrer une invite de commande/shell (Sur Windows, `⊞`+`R`, puis entrer `cmd`).

Exécuter la commande [`poetry shell`](https://python-poetry.org/docs/cli/#shell) qui génére une nouvelle invite de commande utilisant un environnement virtuel python avec toutes les dépendances du projet.

Puis, [`poetry install`](https://python-poetry.org/docs/cli/#install) qui va installer les dépendances.

#### Ajouter une nouvelle dépendance

Pour indiquer à poetry qu'on utilise un package, ne pas oublier d'utiliser la commande [`poetry add`](https://python-poetry.org/docs/cli/#add) suivi du nom du package.

### Générer la base de données

Faire `manage.py migrate`

#### Fixtures

https://docs.djangoproject.com/en/3.1/howto/initial-data/

Permet de charger des données initial

Pour dump les données (dans un dossier fixtures !!!)

`manage.py dumpdata $BDNAME$ > app/fixtures/$FILENAME$.json`

Pour charger les données

`manage.py loaddata $FILENAME$`

#### Charger les datasets et les thèmes de data.namur

`manage.py load_themes` charge tout les thèmes
`manage.py load_datasets` charge tout les datasets (prends un peu de temps attention !!)

### Démarrer le serveur

`manage.py runserver` puis se rendre sur http://127.0.0.1:8000
