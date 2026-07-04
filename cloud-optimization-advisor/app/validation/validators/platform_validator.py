from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_vm_sku import (
    AzureVmSku,
)

from app.models.validation_result import (
    ValidationResult,
)


class PlatformValidator:
    """
    Validates platform compatibility between
    the current VM workload and a candidate SKU.
    """

    DOMAIN = "Platform"

    ####################################################################
    # Public API
    ####################################################################

    def validate(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> list[ValidationResult]:

        return [

            self._validate_hyperv_generation(
                vm,
                candidate,
            ),

            self._validate_cpu_architecture(
                vm,
                candidate,
            ),

            self._validate_ephemeral_os_disk(
                vm,
                candidate,
            ),
        ]
    ####################################################################
    # Helpers
    ####################################################################

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
    def _validate_hyperv_generation(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationResult:

        #
        # Current VM does not require
        # a specific Hyper-V generation.
        #

        if not vm.platform_profile.hyperv_generation:

            return self._result(
                rule="Hyper-V Generation",
                passed=True,
                blocker=False,
                message=(
                    "Current VM does not require "
                    "a specific Hyper-V generation."
                ),
            )

        supported = candidate.capability(
            "HyperVGenerations",
            "",
        )

        passed = (
            vm.platform_profile.hyperv_generation
            in supported
        )

        if passed:

            return self._result(
                rule="Hyper-V Generation",
                passed=True,
                blocker=False,
                message=(
                    "Candidate supports the required "
                    "Hyper-V generation."
                ),
            )

        return self._result(
            rule="Hyper-V Generation",
            passed=False,
            blocker=True,
            message=(
                "Candidate does not support the required "
                "Hyper-V generation."
            ),
        )
        
    def _validate_cpu_architecture(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationResult:

        if not vm.platform_profile.cpu_architecture:

            return self._result(
                rule="CPU Architecture",
                passed=True,
                blocker=False,
                message=(
                    "Current VM does not require "
                    "a specific CPU architecture."
                ),
            )

        candidate_arch = candidate.capability(
            "CpuArchitectureType",
            "",
        )

        passed = (
            candidate_arch.lower()
            == vm.platform_profile.cpu_architecture.lower()
        )

        if passed:

            return self._result(
                rule="CPU Architecture",
                passed=True,
                blocker=False,
                message=(
                    "Candidate supports the required "
                    "CPU architecture."
                ),
            )

        return self._result(
            rule="CPU Architecture",
            passed=False,
            blocker=True,
            message=(
                "Candidate does not support the required "
                "CPU architecture."
            ),
        )
    def _validate_ephemeral_os_disk(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationResult:

        if not vm.platform_profile.ephemeral_os_disk:

            return self._result(
                rule="Ephemeral OS Disk",
                passed=True,
                blocker=False,
                message=(
                    "Current VM does not require "
                    "an Ephemeral OS Disk."
                ),
            )

        passed = candidate.capability_bool(
            "EphemeralOSDiskSupported"
        )

        if passed:

            return self._result(
                rule="Ephemeral OS Disk",
                passed=True,
                blocker=False,
                message=(
                    "Candidate supports "
                    "Ephemeral OS Disk."
                ),
            )

        return self._result(
            rule="Ephemeral OS Disk",
            passed=False,
            blocker=True,
            message=(
                "Candidate does not support "
                "Ephemeral OS Disk."
            ),
        )    