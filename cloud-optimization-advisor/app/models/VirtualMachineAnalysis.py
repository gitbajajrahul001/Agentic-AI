from pydantic import BaseModel, Field

from app.models.recommendation_reason import (
    RecommendationReason,
)

from app.recommendation.recommendation_action import (
    RecommendationAction,
)

from app.recommendation.recommendation_confidence import (
    RecommendationConfidence,
)


class VirtualMachineAnalysis(BaseModel):
    """
    Result of analysing a virtual machine.
    """

    ####################################################################
    # Recommendation
    ####################################################################

    recommendation: RecommendationAction = (
        RecommendationAction.KEEP_CURRENT_SIZE
    )

    confidence: RecommendationConfidence = (
        RecommendationConfidence.MEDIUM
    )

    ####################################################################
    # VM Sizes
    ####################################################################

    current_vm_size: str = ""

    recommended_vm_size: str = ""

    ####################################################################
    # Legacy observations
    # (to be replaced by structured reasons)
    ####################################################################

    observations: list[str] = Field(
        default_factory=list
    )

    ####################################################################
    # Explainability
    ####################################################################

    reasons: list[RecommendationReason] = Field(
        default_factory=list
    )

    ####################################################################
    # Validation
    ####################################################################

    validation_results: list = Field(
        default_factory=list
    )