from dataclasses import dataclass


@dataclass
class ValidationResult:
    """
    Result returned by a single validation rule.
    """

    domain: str
    
    rule: str

    passed: bool

    blocker: bool

    message: str