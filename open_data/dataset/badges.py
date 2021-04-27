from abc import ABCMeta

from badge.base import Badge, BadgeDetail, BadgeAwarded
from badge.stereotypes import ThresholdedBadge, OnceBadge


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
