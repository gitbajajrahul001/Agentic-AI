from app.validation.validators.premium_ssd_validator import (
    PremiumSSDValidator,
)


class RecommendationValidator:

    def __init__(self):

        self.validators = [
            PremiumSSDValidator(),
        ]

    def validate(
        self,
        virtual_machine,
        analysis,
    ):

        results = []

        for validator in self.validators:

            results.append(
                validator.validate(
                    virtual_machine,
                    analysis,
                )
            )

        return results