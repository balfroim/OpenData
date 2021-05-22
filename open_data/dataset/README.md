# OpenData

## Application `dataset`

Cette application contient tous les modèles et vues relatifs aux jeux de données.

### Modèles

Les jeux de données ne sont pas stockés dans leur entièreté dans la base de données. En effet, nous ne gardons que les métadonnées relatives qui forment donc un lien vers la plateforme data.namur.be (les URLS concernées se trouvent dans [le fichier settings.py du projet](../open_data/settings.py)). Ces données sont stockées dans le modèle `ProxyDataset`.

Chaque jeu de données est lié à un thème général.

Les jeux de données peuvent avoir différents types de présentation : tableau, carte, analyse, calendrier, personnalisé, vulgarisé. Les cinq premiers correspondent aux vues disponibles sur data.namur.be. Quant aux vues vulgarisées, il s'agit simplement [de pages HTML statiques](templates/popularized) à rédiger à la main.

Enfin, un jeu de données peut avoir des actualités liées (un lien HTTP vers un article représenté par le modèle `NewsArticle`); et des liens vers d'autres jeux de données (soit automatiquement via des mots-clés, soit manuellement via le modèle `DatasetLink`).

### Commandes

* `manage.py load_themes` : Charge les différents thèmes disponibles depuis data.namur.be.
* `managae.py load_datasets` : Charge les différents jeux de données depuis data.namur.be. De plus, cette commande génère tous les mots-clés liés aux datasets. Ces derniers sont utilisés dans la fonction de recherche et dans les recommandations de jeux de données liés.
