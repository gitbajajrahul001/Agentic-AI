from enum import Enum


class RecommendationConfidence(str, Enum):
    """
    Confidence level for a recommendation.
    """

    HIGH = "HIGH"

    MEDIUM = "MEDIUM"

    LOW = "LOW"