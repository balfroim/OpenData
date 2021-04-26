from badge.base import BadgeDetail
from badge.stereotypes import ThresholdedBadge


class LikedDatasetBadge(ThresholdedBadge):
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

    def thresholded_value(self, user):
        return user.profile.liked_datasets.count()
