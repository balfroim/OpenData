# OpenData

## Application `quiz`

Cette application contient tous les modèles et vues relatives aux quiz.

### Page

Quand une réponse à un quiz est soumise, une requête AJAX est effectuée par le client. Le serveur répond alors avec un fragment HTML qui est inséré à la place du quiz dans la page. Ce fragment contient le formulaire rempli et corrigé.

### Modèles

Un quiz (`Quiz`) peut comprendre plusieurs questions (`Question`) et chaque question peut avoir plusieurs réponses (`Answer`). En effet, il avait été prévu au début qu'un quiz puisse avoir plusieurs questions ainsi que des réponses multiples. L'architecture le permet. Cependant, il a été choisi au final de présenter que des quiz à une seule question et une seule réponse.

À chaque fois qu'un utilisateur soumet une réponse, un objet `QuizSubmission` est créé. Il s'agit des réponses d'un utilisateur pour un quiz donné.

Chaque quiz est lié à un jeu de données en particulier.

Pour créer et modifier des quiz, il est nécessaire dans l'état actuel de la plateforme de passer par l'interface administrateur de Django (route "/admin").
