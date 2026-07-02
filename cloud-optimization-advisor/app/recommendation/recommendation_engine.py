from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_virtual_machine_metrics import (
    AzureVirtualMachineMetrics,
)

from app.models.VirtualMachineAnalysis import (
    VirtualMachineAnalysis,
)

from app.recommendation.recommendation_action import (
    RecommendationAction,
)

from app.recommendation.recommendation_confidence import (
    RecommendationConfidence,
)


class RecommendationEngine:
    """
    Evaluates collected telemetry against policy
    and produces a recommendation.
    """

    def __init__(
        self,
        policy: dict,
    ):

        self.policy = policy

    ####################################################################
    # Public API
    ####################################################################

    def analyze(
        self,
        vm: AzureVirtualMachine,
        metrics: AzureVirtualMachineMetrics,
    ) -> VirtualMachineAnalysis:

        analysis = VirtualMachineAnalysis()

        analysis.current_vm_size = vm.vm_size

        #
        # Rule 1
        # Enough telemetry?
        #

        minimum_sample_count = self.policy[
            "telemetry"
        ][
            "minimum_sample_count"
        ]

        if (
            metrics.sample_count <
            minimum_sample_count
        ):

            analysis.recommendation = (
                RecommendationAction.INSUFFICIENT_DATA
            )

            analysis.confidence = (
                RecommendationConfidence.LOW
            )

            analysis.observations.append(
                "Insufficient telemetry to produce a reliable recommendation."
            )

            return analysis

        #
        # Rule 2
        # CPU Pressure
        #

        cpu_upsize_threshold = self.policy[
            "decision"
        ][
            "cpu"
        ][
            "upsize_threshold"
        ]

        if (
            metrics.cpu_average_percent >=
            cpu_upsize_threshold
        ):

            analysis.recommendation = (
                RecommendationAction.UPSIZE
            )

            analysis.confidence = (
                RecommendationConfidence.HIGH
            )

            analysis.observations.append(
                f"Average CPU utilization ({metrics.cpu_average_percent:.2f}%) exceeds the configured threshold."
            )

            return analysis

        #
        # Rule 3
        # Memory Pressure
        #

        memory_upsize_threshold = self.policy[
            "decision"
        ][
            "memory"
        ][
            "upsize_threshold"
        ]

        if (
            metrics.memory_average_percent >=
            memory_upsize_threshold
        ):

            analysis.recommendation = (
                RecommendationAction.UPSIZE
            )

            analysis.confidence = (
                RecommendationConfidence.HIGH
            )

            analysis.observations.append(
                f"Average memory utilization ({metrics.memory_average_percent:.2f}%) exceeds the configured threshold."
            )

            return analysis

        #
        # Rule 4
        # Safe Downsize
        #

        cpu_downsize_threshold = self.policy[
            "decision"
        ][
            "cpu"
        ][
            "downsize_threshold"
        ]

        memory_downsize_threshold = self.policy[
            "decision"
        ][
            "memory"
        ][
            "downsize_threshold"
        ]

        if (
            metrics.cpu_average_percent <
            cpu_downsize_threshold
            and
            metrics.memory_average_percent <
            memory_downsize_threshold
        ):

            analysis.recommendation = (
                RecommendationAction.DOWNSIZE
            )

            analysis.confidence = (
                RecommendationConfidence.HIGH
            )

            analysis.observations.append(
                "CPU and Memory utilization are below the configured thresholds."
            )

            return analysis

        #
        # Rule 5
        # Default
        #

        analysis.recommendation = (
            RecommendationAction.KEEP_CURRENT_SIZE
        )

        analysis.confidence = (
            RecommendationConfidence.MEDIUM
        )

        analysis.observations.append(
            "Current utilization is within configured operating thresholds."
        )

        return analysis