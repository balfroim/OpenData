from badge.base import Badge, BadgeAwarded


def check_threshold(levels, thresholds, observed_value):
    award = None
    for lvl in range(len(levels)):
        if observed_value >= thresholds[lvl]:
            award = BadgeAwarded(level=lvl+1)
    return award


class QuizFailedBadge(Badge):
    slug = "quiz-fail"
    levels = [
        # Se tromper dans un quiz
        "Error humanum est",
        # Se tromper dans 5 quiz
        "Persevare diabolicum"
    ]
    level_thresholds = [
        1,
        5
    ]
    events = [
        "on_quiz_result"
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        nb_failed_quizzes = len([quiz for quiz in user.quizzes_taken.all() if not quiz.is_perfect_score])
        return check_threshold(self.levels, self.level_thresholds, nb_failed_quizzes)


class QuizPerfectBadge(Badge):
    slug = "quiz-perfect"
    levels = [
        # Répondre parfaitement à un quiz
        "Question pour un champion",
        # Répondre parfaitement à 5 quiz
        "Veni, Vidi, Vici"
    ]
    level_thresholds = [
        1,
        5
    ]
    events = [
        "on_quiz_result"
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        nb_perfect_score_quizzes = len([quiz for quiz in user.quizzes_taken.all() if quiz.is_perfect_score])
        return check_threshold(self.levels, self.level_thresholds, nb_perfect_score_quizzes)
