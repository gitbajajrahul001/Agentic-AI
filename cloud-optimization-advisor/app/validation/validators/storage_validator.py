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

    RULE_MAX_DATA_DISKS = "Maximum Data Disks"

    RULE_PREMIUM_STORAGE = "Premium Storage"

    RULE_ULTRA_SSD = "Ultra SSD"

    ####################################################################
    # Public API
    ####################################################################

    def validate(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> list[ValidationResult]:

        return [

            self._validate_max_data_disks(
                vm,
                candidate,
            ),

            self._validate_premium_storage(
                vm,
                candidate,
            ),

            self._validate_ultra_ssd(
                vm,
                candidate,
            ),

        ]    
    
    def _result(
        self,
        rule: str,
        passed: bool,
        blocker: bool,
        message: str,
    ) -> ValidationResult:

        return ValidationResult(

            domain=self.DOMAIN,

            rule=rule,

            passed=passed,

            blocker=blocker,

            message=message,
        )

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

        candidate_max = candidate.capability_int(
            "MaxDataDiskCount"
        )

        passed = (
            current_disks <= candidate_max
        )

        if passed:

            return self._result(

                rule=self.RULE_MAX_DATA_DISKS,

                passed=True,

                blocker=False,

                message=(
                    f"Candidate supports "
                    f"{candidate_max} data disks."
                ),
            )

        return self._result(

            rule=self.RULE_MAX_DATA_DISKS,

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
        # Current VM does not require Premium SSD.
        #

        if not vm.storage_profile.has_premium_ssd:

            return self._result(

                rule=self.RULE_PREMIUM_STORAGE,

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

            return self._result(

                rule=self.RULE_PREMIUM_STORAGE,

                passed=True,

                blocker=False,

                message=(
                    "Candidate supports Premium SSD."
                ),
            )

        return self._result(

            rule=self.RULE_PREMIUM_STORAGE,

            passed=False,

            blocker=True,

            message=(
                "Candidate does not support Premium SSD."
            ),
        )
    def _validate_ultra_ssd(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationResult:

        #
        # Current VM does not require Ultra SSD.
        #

        if not vm.storage_profile.has_ultra_ssd:

            return self._result(

                rule=self.RULE_ULTRA_SSD,

                passed=True,

                blocker=False,

                message=(
                    "Current VM does not require Ultra SSD."
                ),
            )

        passed = candidate.capability_bool(
            "UltraSSDAvailable"
        )

        if passed:

            return self._result(

                rule=self.RULE_ULTRA_SSD,

                passed=True,

                blocker=False,

                message=(
                    "Candidate supports Ultra SSD."
                ),
            )

        return self._result(

            rule=self.RULE_ULTRA_SSD,

            passed=False,

            blocker=True,

            message=(
                "Candidate does not support Ultra SSD."
            ),
        )  