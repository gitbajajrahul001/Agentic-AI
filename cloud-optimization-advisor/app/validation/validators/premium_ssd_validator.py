from app.models.validation_result import (
    ValidationResult,
)


class PremiumSSDValidator:

    def validate(
        self,
        virtual_machine,
    ) -> ValidationResult:

        return ValidationResult(
            validator="Premium SSD",
            passed=True,
            blocker=False,
            reason="Validation not implemented yet.",
        )