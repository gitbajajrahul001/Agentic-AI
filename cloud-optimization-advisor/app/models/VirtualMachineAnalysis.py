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

from app.models.validation_summary import (
    ValidationSummary,
)
from app.models.candidate_evaluation import (
    CandidateEvaluation,
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
    # Explainability
    ####################################################################

    reasons: list[RecommendationReason] = Field(
        default_factory=list
    )

    ####################################################################
    # Candidate Evaluation
    ####################################################################

    candidate_evaluations: list[
        CandidateEvaluation
    ] = Field(
        default_factory=list
    )