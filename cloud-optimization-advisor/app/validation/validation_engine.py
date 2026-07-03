from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_vm_sku import (
    AzureVmSku,
)


class ValidationEngine:
    """
    Validates whether a candidate VM SKU is
    compatible with the current virtual machine.

    Each validation rule is implemented as an
    independent method.
    """

    ####################################################################
    # Public API
    ####################################################################

    def validate(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> bool:

        if not self._validate_premium_ssd(
            vm,
            candidate,
        ):
            return False

        return True

    ####################################################################
    # Validation Rules
    ####################################################################

    def _validate_premium_ssd(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> bool:
        """
        If the current VM uses Premium SSD,
        the candidate SKU must support Premium IO.
        """

        #
        # VM is not using Premium SSD.
        #
        if not vm.storage_profile.has_premium_ssd:
            return True

        #
        # Candidate must support Premium IO.
        #
        return candidate.capability_bool(
            "PremiumIO"
        )