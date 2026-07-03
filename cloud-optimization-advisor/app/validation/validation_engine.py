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

    MVP:
    Always returns True.

    Validation rules will be added incrementally.
    """

    ####################################################################
    # Public API
    ####################################################################

    def validate(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> bool:

        return True