from badge.base import Badge, BadgeDetail, BadgeAwarded


def check_threshold(levels, thresholds, observed_value):
    award = None
    for lvl in range(len(levels)):
        if observed_value >= thresholds[lvl]:
            award = BadgeAwarded(level=lvl+1)
    return award


class QuizFailedBadge(Badge):
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
    multiple = False

    def award(self, **state):
        user = state["user"]
        nb_failed_quizzes = len([quiz for quiz in user.quizzes_taken.all() if not quiz.is_perfect_score])
        award = check_threshold(self.levels, self.level_thresholds, nb_failed_quizzes)
        if award:
            score = self.levels[award.level].score
            user.profile.add_score(score)
            print(f'{user.profile.score} (+ {score})')
            return award


class QuizPerfectBadge(Badge):
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
    multiple = False

    def award(self, **state):
        user = state["user"]
        nb_perfect_score_quizzes = len([quiz for quiz in user.quizzes_taken.all() if quiz.is_perfect_score])
        award = check_threshold(self.levels, self.level_thresholds, nb_perfect_score_quizzes)
        if award:
            score = self.levels[award.level].score
            print(self.levels[award.level])
            user.profile.add_score(score)
            print(f'{user.profile.score} (+ {score})')
            return award
