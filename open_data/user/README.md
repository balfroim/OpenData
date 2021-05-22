# OpenData

## Application `user`

Cette application contient tous les modèles et vues relatifs à la gestion des utilisateurs.

### Modèles

La gestion des utilisateurs est directement réalisée en utilisant [le module Django qui y est dédié](https://docs.djangoproject.com/fr/3.2/topics/auth/).

Cependant, le modèle `User` a été redéfini. L'adresse e-mail est utilisée comme identifiant de connexion alors que le champ `username` est généré de manière aléatoire. De plus, un modèle `Profile` est utilisé pour stocker le nom d'utilisateur ainsi que sa description affichés sur la plateforme. Une instance de `Profile` est toujours créée en même temps qu'un utilisateur en utilisant un `Manager` personnalisé.

De cette manière, plusieurs utilisateurs peuvent avoir le même nom, à condition que leurs adresses e-mail sont différentes.

### Utilisateurs anonymes

La plateforme peut être utilisée en tant qu'utilisateur anonyme. Cela est rendu possible par [l'utilisation d'un middleware](https://docs.djangoproject.com/fr/3.2/topics/http/middleware/) : quand une requête est effectuée sur n'importe quelle route de la plateforme et qu'elle n'est pas authentifiée, le serveur crée automatiquement un utilisateur et l'authentifie. Le champ `is_registered` est alors mis à `False`.

Cela permet aux utilisateurs de gagner, par exemple, des badges sans devoir se créer activement un compte. Dans les faits, leur compte est déjà créé mais l'utilisateur n'en a pas l'impression.

Ensuite, en soumettant le formulaire d'inscription, le champ `is_registered` est passé à `True` et le nom, l'adresse e-mail, et le mot de passe du compte sont mis à jour. L'utilisateur a donc l'impression de s'être créé un compte et d'avoir sauvegardé ses badges alors qu'il s'est en fait juste créé des identifiants.
