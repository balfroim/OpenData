OpenData

## DEV

### Installer les dépendances

D'abord installer poetry en suivant les instructions de cette [page](https://python-poetry.org/docs/#installation). C'est un outil qui nous permets de gérer facilement les dépendances du projet. 

Ensuite, depuis le dossier open_data, démarrer un shell pour exécuter la commande `poetry shell` qui va démarrer un nouveau shell à l'intérieur d'un environnement virtuel python (si il n'existe pas encore, poetry va la créer donc ça risque de prendre un peu de temps la première fois.) avec toutes les packages et leurs dépendances du projet.

Pour indiquer à poetry qu'on utilise un package, ne pas oublier d'utiliser la commande `poetry add` suivi du nom du package. Plus d'infos sur cette [page](https://python-poetry.org/docs/cli/#add).

### Démarrer le serveur

`manage.py runserver` puis se rendre sur http://127.0.0.1:8000



### Fixtures

https://docs.djangoproject.com/en/3.1/howto/initial-data/

Permet de charger des données initial

Pour dump les données (dans un dossier fixtures !!!)

`manage.py dumpdata $BDNAME$ > app/fixtures/$FILENAME$.json`

Pour charger les données

`manage.py loaddata $FILENAME$`