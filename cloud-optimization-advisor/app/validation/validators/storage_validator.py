from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_vm_sku import (
    AzureVmSku,
)

from app.models.validation_result import (
    ValidationResult,
)


class StorageValidator:
    """
    Validates storage compatibility between
    the current VM workload and a candidate SKU.
    """

    DOMAIN = "Storage"

    ####################################################################
    # Public API
    ####################################################################

    def validate(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> list[ValidationResult]:

        results = []

        results.append(
            self._validate_max_data_disks(
                vm,
                candidate,
            )
        )

        results.append(
            self._validate_premium_storage(
                vm,
                candidate,
            )
        )

        return results

    ####################################################################
    # Validation Rules
    ####################################################################

    def _validate_max_data_disks(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationResult:

        current_disks = (
            vm.storage_profile.data_disk_count
        )

        candidate_max = int(
            candidate.capabilities.get(
                "MaxDataDiskCount",
                0,
            )
        )

        passed = (
            current_disks <= candidate_max
        )

        if passed:

            return ValidationResult(

                domain=self.DOMAIN,

                rule="Maximum Data Disks",

                passed=True,

                blocker=False,

                message=(
                    f"Candidate supports "
                    f"{candidate_max} data disks."
                ),
            )

        return ValidationResult(

            domain=self.DOMAIN,

            rule="Maximum Data Disks",

            passed=False,

            blocker=True,

            message=(
                f"Candidate supports "
                f"{candidate_max} data disks "
                f"but the current VM uses "
                f"{current_disks}."
            ),
        )

    def _validate_premium_storage(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationResult:

        #
        # VM doesn't require Premium SSD.
        #

        if not vm.storage_profile.has_premium_ssd:

            return ValidationResult(

                domain=self.DOMAIN,

                rule="Premium Storage",

                passed=True,

                blocker=False,

                message=(
                    "Current VM does not require Premium SSD."
                ),
            )

        passed = candidate.capability_bool(
            "PremiumIO"
        )

        if passed:

            return ValidationResult(

                domain=self.DOMAIN,

                rule="Premium Storage",

                passed=True,

                blocker=False,

                message=(
                    "Candidate supports Premium SSD."
                ),
            )

        return ValidationResult(

            domain=self.DOMAIN,

            rule="Premium Storage",

            passed=False,

            blocker=True,

            message=(
                "Candidate does not support Premium SSD."
            ),
        )