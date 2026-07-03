from dataclasses import field

from pydantic import BaseModel, Field

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

    recommendation: RecommendationAction = (
        RecommendationAction.KEEP_CURRENT_SIZE
    )

    confidence: RecommendationConfidence = (
        RecommendationConfidence.MEDIUM
    )

    observations: list[str] = Field(
        default_factory=list
    )

    current_vm_size: str = ""

    recommended_vm_size: str = ""

    validation_results: list = field(default_factory=list)