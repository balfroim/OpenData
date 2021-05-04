from abc import ABCMeta

from badge.base import Badge, BadgeDetail, BadgeAwarded
from badge.stereotypes import ThresholdedBadge, OnceBadge

def check_threshold(levels, thresholds, observed_value):
    award = None
    for lvl in range(len(levels)):
        if observed_value >= thresholds[lvl]:
            award = BadgeAwarded(level=lvl+1)
    return award

class LikeDatasetBadge(ThresholdedBadge):
    slug = 'dataset-like'
    levels = [
        BadgeDetail(
            name="J'aime donc je suis",
            description='Liker un jeu de données.',
            score=10
        ),
        BadgeDetail(
            name='Open relationship',
            description='Liker cinq jeux de données.',
            score=50
        ),
    ]
    level_thresholds = [
        1,
        5,
    ]
    events = [
        'on_dataset_like',
    ]

    def thresholded_value(self, user):
        return user.profile.liked_datasets.count()


class QuizDatasetInspection(OnceBadge):
    slug = 'quiz-dataset-inspection'
    levels = [
        BadgeDetail(
            name='La curiosité est un bon défaut',
            description='Inspecter le jeu de données lié à un quiz.',
            score=20
        ),
    ]
    events = [
        'on_linked_quiz_inspect',
    ]


class DownloadDatasetBadge(OnceBadge):
    slug = 'dataset-download'
    levels = [
        BadgeDetail(
            name='Données ouvertes',
            description='Télécharger un jeu de données.',
            score=80
        ),
    ]
    events = [
        'on_dataset_download',
    ]


class FirstCommentDatasetBadge(Badge, metaclass=ABCMeta):
    slug = 'dataset-first-comment'
    levels = [
        BadgeDetail(
            name='First !',
            description='Être le premier à commenter un jeu de données.',
            score=200
        ),
    ]
    events = [
        'on_question_ask',
    ]
    multiple = False

    def award(self, **states):
        dataset = states['dataset']
        if dataset.questions.count() == 1:
            return BadgeAwarded(level=1)
        return None


class SubscribeThemeBadge(ThresholdedBadge):
    slug = 'theme-subscribe'
    levels = [
        BadgeDetail(
            name="Intéressant ?",
            description='S\'abonner à un thème.',
            score=10
        ),
        BadgeDetail(
            name='Stay tuned',
            description='S\'abonner à cinq thèmes.',
            score=50
        ),
        BadgeDetail(
            name='Rule them all',
            description='S\'abonner à dix thèmes.',
            score=50
        ),
    ]
    level_thresholds = [
        1,
        5,
        10,
    ]
    events = [
        'on_theme_subscription',
    ]

    def thresholded_value(self, user):
            return user.profile.theme_subscriptions.count()


class ExploreDatasetBadge(ThresholdedBadge):
    slug = 'dataset-explore'
    levels = [
        BadgeDetail(
            name="Touriste",
            description='Explorer 1 datasets.',
            score=10
        ),
        BadgeDetail(
            name='Explorateur',
            description='Explorer 5 datasets.',
            score=40
        ),
        BadgeDetail(
             name='Globetrotter',
             description='Explorer 10 datasets.',
             score=50
        ),
    ]
    level_thresholds = [
        1,
        5,
        10,
    ]
    events = [
        'on_dataset_explore',
    ]

    def thresholded_value(self, user):
        #TODO
        return 0


class VisitedAllThemeDatasetBadge(Badge, metaclass=ABCMeta):
    slug = 'dataset-first-comment'
    levels = [
        BadgeDetail(
            name='Le tour de la question',
            description='Explorer au moins un dataset par thème.',
            score=100
        ),
    ]
    events = [
        'on_dataset_explore',
    ]

class AskQuestionBadge(ThresholdedBadge):
    slug = 'question-ask'
    levels = [
        BadgeDetail(
            name='Il n\'y a pas de question bête',
            description='Poser une question',
            score=20
        ),
        BadgeDetail(
            name='non sérieusement continue à poser des questions',
            description='Poser 20 questions.',
            score=100
        ),
        BadgeDetail(
            name='Bon il y a des limites quand même....',
            description='Poser 50 questions.',
            score=200
        ),
    ]
    level_thresholds = [
            1,
            20,
            50,
    ]
    events = [
        'on_question_ask',
    ]
    def thresholded_value(self, user):
            #TODO
            return 0


class AnswerQuestionBadge(ThresholdedBadge):
    slug = 'question-answer'
    levels = [
        BadgeDetail(
            name='Le savoir c\'est comme la confiture...',
            description='Répondre à une question',
            score=20
        ),
        BadgeDetail(
            name='...moins on en a...',
            description='Répondre à 20 questions.',
            score=100
        ),
        BadgeDetail(
            name='...plus on l\'étale.',
            description='Répondre à 50 questions.',
            score=200
        ),
    ]
    level_thresholds = [
            1,
            20,
            50,
    ]
    events = [
        'on_question_answer',
    ]

    def thresholded_value(self, user):
            #TODO
            return 0
