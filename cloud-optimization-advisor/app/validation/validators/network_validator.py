from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_vm_sku import (
    AzureVmSku,
)

from app.models.validation_result import (
    ValidationResult,
)


class NetworkValidator:
    """
    Validates network compatibility between
    the current VM workload and a candidate SKU.
    """

    DOMAIN = "Network"

    ####################################################################
    # Public API
    ####################################################################

    def validate(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> list[ValidationResult]:

        return [

            self._validate_accelerated_networking(
                vm,
                candidate,
            ),

            self._validate_network_interfaces(
                vm,
                candidate,
            ),

        ]

    ####################################################################
    # Validation Rules
    ####################################################################

    def _validate_accelerated_networking(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationResult:

        #
        # Current VM does not require
        # Accelerated Networking.
        #

        if (
            not vm.network_profile
            .accelerated_networking_enabled
        ):

            return self._result(
                rule="Accelerated Networking",
                passed=True,
                blocker=False,
                message=(
                    "Current VM does not require "
                    "Accelerated Networking."
                ),
            )

        passed = candidate.capability_bool(
            "AcceleratedNetworkingEnabled"
        )

        if passed:

            return self._result(
                rule="Accelerated Networking",
                passed=True,
                blocker=False,
                message=(
                    "Candidate supports "
                    "Accelerated Networking."
                ),
            )

        return self._result(
            rule="Accelerated Networking",
            passed=False,
            blocker=True,
            message=(
                "Candidate does not support "
                "Accelerated Networking."
            ),
        )

    def _validate_network_interfaces(
        self,
        vm: AzureVirtualMachine,
        candidate: AzureVmSku,
    ) -> ValidationResult:

        current_nics = (
            vm.network_profile.network_interface_count
        )

        candidate_max = candidate.capability_int(
            "MaxNetworkInterfaces"
        )

        passed = (
            current_nics <= candidate_max
        )

        if passed:

            return self._result(
                rule="Maximum Network Interfaces",
                passed=True,
                blocker=False,
                message=(
                    f"Candidate supports "
                    f"{candidate_max} network "
                    f"interface(s)."
                ),
            )

        return self._result(
            rule="Maximum Network Interfaces",
            passed=False,
            blocker=True,
            message=(
                f"Candidate supports "
                f"{candidate_max} network "
                f"interface(s), but the current "
                f"VM uses {current_nics}."
            ),
        )

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