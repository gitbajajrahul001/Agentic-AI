from dataclasses import dataclass


@dataclass
class ValidationResult:
    """
    Result returned by a single validator.
    """

    validator: str

    passed: bool

    blocker: bool

    reason: str