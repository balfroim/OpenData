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
        print(quiz_submission_count)
        if quiz_submission_count >= 25:
            return BadgeAwarded(level=3)
        elif quiz_submission_count >= 10:
            return BadgeAwarded(level=2)
        elif quiz_submission_count >= 1:
            return BadgeAwarded(level=1)


