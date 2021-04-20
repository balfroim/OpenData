from badge.base import Badge, BadgeAwarded


def check_threshold(levels, thresholds, observed_value):
    award = None
    for lvl in range(len(levels)):
        if observed_value >= thresholds[lvl]:
            award = BadgeAwarded(level=lvl+1)
    return award


class LikedDatasetBadge(Badge):
    slug = "dataset-like"
    levels = [
        # Liker un dataset
        "J'aime donc je suis",
        # Liker 5 datasets
        "Open relationship"
    ]
    level_thresholds = [
        1,
        5
    ]
    events = [
        "on_dataset_liked"
    ]
    multiple = False

    def award(self, **state):
        user = state["user"]
        nb_liked_dataset = len(user.profile.liked_datasets.all())
        return check_threshold(self.levels, self.level_thresholds, nb_liked_dataset)
