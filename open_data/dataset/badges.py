from badge.base import Badge, BadgeDetail, BadgeAwarded


def check_threshold(levels, thresholds, observed_value):
    award = None
    for lvl in range(len(levels)):
        if observed_value >= thresholds[lvl]:
            award = BadgeAwarded(level=lvl+1)
    return award


class LikedDatasetBadge(Badge):
    slug = "dataset-like"
    levels = [
        BadgeDetail(
            name="J'aime donc je suis",
            description="Liker un dataset.",
            score=10
        ),
        BadgeDetail(
            name="Open relationship",
            description="Liker cinq datasets.",
            score=50
        ),
    ]
    level_thresholds = [
        1,
        5,
    ]
    events = [
        "on_dataset_like",
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        nb_liked_dataset = len(user.profile.liked_datasets.all())
        award = check_threshold(self.levels, self.level_thresholds, nb_liked_dataset)
        if award:
            score = self.levels[award.level].score
            user.profile.add_score(score)
            print(f'{user.profile.score} (+ {score})')
            return award
