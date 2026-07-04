from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_vm_sku import (
    AzureVmSku,
)

from app.models.validation_summary import (
    ValidationSummary,
)

from app.validation.validators.storage_validator import (
    StorageValidator,
)

from app.validation.validators.network_validator import (
    NetworkValidator,
)

from app.validation.validators.platform_validator import (
    PlatformValidator,
)

# Future
#
# from app.validation.validators.network_validator import (
#     NetworkValidator,
# )
#
# from app.validation.validators.security_validator import (
#     SecurityValidator,
# )
#
# from app.validation.validators.compute_validator import (
#     ComputeValidator,
# )


class ValidationEngine:
    """
    Executes all validation domains and
    aggregates the results.
    """

    def __init__(self):

        self.validators = [

            StorageValidator(),
            NetworkValidator(),
            PlatformValidator(),

            #
            # Future validators
            # SecurityValidator(),
            # ComputeValidator(),
        ]

    ####################################################################
    # Public API
    ####################################################################

    def validate(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationSummary:

        summary = ValidationSummary()

        for validator in self.validators:

            results = validator.validate(
                vm,
                candidate,
            )

            summary.results.extend(
                results
            )

        summary.passed = all(

            result.passed

            for result in summary.results

            if result.blocker

        )

        return summary