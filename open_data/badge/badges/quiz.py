from pinax.badges.base import Badge, BadgeAwarded

class QuizBadge(Badge):
    slug = "quiz"
    levels = [
        "Bronze",
        "Silver",
        "Gold",
    ]
    events = [
        "quiz_submit",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        quiz_submission_count = user.quizzes_taken.count()
        award = None
        if quiz_submission_count >= 3:
            award = BadgeAwarded(level=3)
        elif quiz_submission_count >= 2:
            award = BadgeAwarded(level=2)
        elif quiz_submission_count >= 1:
            award = BadgeAwarded(level=1)
        return award


