# OpenData

## Application `badge`

Cette application contient tous les modèles et vues relatifs au décernement de badges. Le code source se base sur [le module pinax-badges](https://github.com/pinax/pinax-badges) publié sous licence MIT. Nous remercions [ses auteurs originaux](AUTHORS) pour leur travail.

Pour la gestion des notifications relatives aux badges, l'application utilise également [django-notifications](https://github.com/django-notifications/django-notifications) publié sous licence BSD.

Pour plus d'informations, veuillez vous référer à ces deux projets.

### Badges

Au démarrage du serveur, [le singleton `BadgeCache`](registry.py) charge tous les fichiers `badges.py` trouvés à la racine des applications. Ces fichiers doivent contenir des classes qui héritent de [la classe abstraite `Badge`](base.py). Elles représentent les différents badges qui peuvent être obtenus sur la plateforme.

De plus, les positions des badges sur la grille sont définis dans [le fichier badges.json](../badges.json).

Pour définir un badge, il suffit donc de créer une classe qui hérite directement de `Badge` et qui définit ses méthodes abstraites (notamment `award` qui sert de prédicat pour déterminer quand un badge est effectivement décerné).

### Stéréotypes de badge

Il existe également [des stéréotypes de badge](stereotypes.py) qui sont des classes abstraites qui peuvent représenter les types de badges les plus répandus :

* `ThresholdedBadge` est un badge à plusieurs niveaux qui vérifie juste si un seuil est dépassé ou non. Il suffit de définir le champ `level_thresholds` (une liste contenant les différents seuils) et la méthode `thresholded_value` (qui renvoie la valeur à comparer aux seuils).
* `OnceBadge` est un badge avec un niveau unique qui ne peut être obtenu qu'une seule fois. Quand l'événement lié est déclenché, le badge est décerné.

### Commandes

* `manage.py collect_badges` : Met à jour un fichier JSON contenant la position de chaque instance de badges. Les badges déjà présents sont conservés. Les badges supprimés sont annotés comme tel dans le but de pouvoir être récupérés par la suite.

### Fun fact

> Ce fichier readme contient le mot "badge" 28 fois.
