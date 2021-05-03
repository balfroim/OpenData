from badge.base import Badge, BadgeDetail, BadgeAwarded
from badge.stereotypes import ThresholdedBadge


class QuizFailedBadge(ThresholdedBadge):
    slug = "quiz-fail"
    levels = [
        BadgeDetail(
            name="Errare humanum est",
            description="Se tromper dans un quiz.",
            image="cancel.png",
            score=5
        ),
        BadgeDetail(
            name="Persevare diabolicum",
            description="Se tromper dans cinq quiz.",
            image="cancel.png",
            score=25
        ),
    ]
    level_thresholds = [
        1,
        5,
    ]
    events = [
        "on_quiz_result",
    ]

    def thresholded_value(self, user):
        return len([quiz for quiz in user.quizzes_taken.all() if not quiz.is_perfect_score])


class QuizPerfectBadge(ThresholdedBadge):
    slug = "quiz-perfect"
    levels = [
        BadgeDetail(
            name="Question pour un champion",
            description="Répondre parfaitement à un quiz.",
            score=20
        ),
        BadgeDetail(
            name="Veni, vidi, vici",
            description="Répondre parfaitement à cinq quiz.",
            score=100
        )
    ]
    level_thresholds = [
        1,
        5,
    ]
    events = [
        "on_quiz_result",
    ]

    def thresholded_value(self, user):
        return len([quiz for quiz in user.quizzes_taken.all() if quiz.is_perfect_score])
