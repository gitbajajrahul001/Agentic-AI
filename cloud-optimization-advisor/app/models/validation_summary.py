from dataclasses import dataclass, field

from app.models.validation_result import (
    ValidationResult,
)


@dataclass
class ValidationSummary:
    """
    Overall validation outcome for a recommendation.
    """

    passed: bool = True

    results: list[ValidationResult] = field(
        default_factory=list
    )