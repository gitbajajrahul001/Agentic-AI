from pydantic import BaseModel

from app.models.validation_summary import (
    ValidationSummary,
)


class CandidateEvaluation(BaseModel):
    """
    Validation outcome for a candidate VM SKU.
    """

    candidate_vm_size: str

    validation_summary: ValidationSummary

    selected: bool = False