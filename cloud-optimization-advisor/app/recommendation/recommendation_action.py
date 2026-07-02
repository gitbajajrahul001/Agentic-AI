from enum import Enum


class RecommendationAction(str, Enum):
    """
    Possible recommendation outcomes.
    """

    UPSIZE = "UPSIZE"

    DOWNSIZE = "DOWNSIZE"

    KEEP_CURRENT_SIZE = "KEEP_CURRENT_SIZE"

    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"