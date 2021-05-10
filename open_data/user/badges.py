from badge.base import BadgeDetail
from badge.stereotypes import ThresholdedBadge, OnceBadge


class UserConnection(ThresholdedBadge):
    slug = 'user-connection'
    levels = [
        BadgeDetail(
            name='Bienvenue',
            description='Se conecter 1 jour',
            score=20
        ),
        BadgeDetail(
            name='Vous, ici?',
            description='Se conecter 10 jours d\'affilé',
            score=20
        ),
        BadgeDetail(
            name='Faites comme chez vous',
            description='Se conecter 50 jours d\'affilé',
            score=100
        ),
    ]
    level_thresholds = [
        1,
        10,
        50,
    ]
    events = [
        'on_user_connection',
    ]


class UserTimeConnection(ThresholdedBadge):
    slug = 'user-time-connection'
    levels = [
        BadgeDetail(
            name='Une petite pause ?',
            description='Rester connecté 30 minutes d\'affilé',
            score=20
        ),
    ]
    events = [
        'on_user_time_connection',
    ]


# class UserDayConnection(OnceBadge):
#     slug = 'user-day-connection'
#     levels = [
#         BadgeDetail(
#             name='Une pomme chaque matin éloigne le médecin',
#             description='Se connecter quotidiennement',
#             score=10
#         ),
#     ]
#     events = [
#         'on_user_day_connection',
#     ]


# class UploadProfilePicture(OnceBadge):
#     slug = 'upload-profile-picture'
#     levels = [
#         BadgeDetail(
#             name='L\'habit ne fait pas le moine',
#             description='Importer une photo de profil',
#             score=20
#         ),
#     ]
#
#     events = [
#         'on_user_picture_upload',
#     ]


class ModifyProfilName(OnceBadge):
    slug = 'modify-profil-name'
    levels = [
        BadgeDetail(
            name='Say my name',
            description='Changer de nom de profil',
            score=20
        ),
    ]

    events = [
        'on_user_profil_name',
    ]


class AddBiography(OnceBadge):
    slug = 'add-biograpy'
    levels = [
        BadgeDetail(
            name='Dis moi qui tu es, je saurai qui tu es.',
            description='Ajouter une biographie',
            score=20
        ),
    ]

    events = [
        'on_user_profil_bio',
    ]


class WinnerBadge(OnceBadge):
    slug = 'be-the-best'
    levels = [
        BadgeDetail(
            name='Veni vidi vici',
            description='Être le premier du tableau des scores',
            score=0
        ),
    ]

    events = [
        'top_1',
    ]


# class PantheonBadge(OnceBadge):
#     slug = 'pantheon'
#     levels = [
#         BadgeDetail(
#             name='Bienvenue, au pantheon des héros',
#             description='Être dans les 20 premiers du tableau des scores et y rester 5 jours',
#             score=200
#         ),
#     ]
#
#     events = [
#         'stay_in_the_light',
#     ]


# class BestWinnerBadge(OnceBadge):
#     slug = 'best-winner'
#     levels = [
#         BadgeDetail(
#             name='Tout le monde veut prendre sa place',
#             description='Être  premier du tableau des scores et y rester 24 heures',
#             score=200
#         ),
#     ]
#
#     events = [
#         'stay_in_the_light',
#     ]


# class PokeBadge(OnceBadge):
#     slug = 'pokebadge'
#     levels = [
#         BadgeDetail(
#             name='Collectionneur',
#             description='Gagner 5 badges',
#             score=200
#         ),
#         BadgeDetail(
#             name='Attraper les tous',
#             description='Gagner tous les badges',
#             score=200
#         ),
#     ]
#     level_thresholds = [
#         5,
#         20,
#     ]
#     events = [
#         'catch_them_all',
#     ]
