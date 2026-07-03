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

from app.models.recommendation_reason import (
    RecommendationReason,
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

####################################################################
# Helpers
####################################################################

    def _add_reason(
        self,
        analysis: VirtualMachineAnalysis,
        category: str,
     message: str,
    ):

     analysis.reasons.append(

        RecommendationReason(

            category=category,

            message=message,
        )
    )


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

            self._add_reason(
                analysis,
                "Insufficient telemetry",
                "...",
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

            self._add_reason(

                analysis,
                "CPU",

                (
                    f"Average CPU utilization "
                    f"({metrics.cpu_average_percent:.2f}%) "
                    f"exceeds the configured upsize "
                    f"threshold ({cpu_upsize_threshold}%)."
                ),
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

            self._add_reason(

                analysis,

                "Memory",

                (
                    f"Average memory utilization "
                    f"({metrics.memory_average_percent:.2f}%) "
                    f"exceeds the configured upsize "
                    f"threshold ({memory_upsize_threshold}%)."
                ),
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

            self._add_reason(

                analysis,

                "CPU",

                (
                    f"Average CPU utilization "
                    f"({metrics.cpu_average_percent:.2f}%) "
                    f"is below the configured downsize "
                    f"threshold ({cpu_downsize_threshold}%)."
                ),
            )
            self._add_reason(

                analysis,

                "Memory",

                (
                    f"Average memory utilization "
                    f"({metrics.memory_average_percent:.2f}%) "
                    f"is below the configured downsize "
                    f"threshold ({memory_downsize_threshold}%)."
                ),
            )

            self._add_reason(

                analysis,

                "Recommendation",

                "The virtual machine qualifies for downsizing.",
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

        self._add_reason(

            analysis,

            "CPU",

            (
                f"Average CPU utilization "
                f"({metrics.cpu_average_percent:.2f}%) "
                f"is below the configured upsize "
                f"threshold ({cpu_upsize_threshold}%) "
                f"and above the configured downsize "
                f"threshold ({cpu_downsize_threshold}%)."
            ),
        )

        self._add_reason(

            analysis,

            "Memory",

            (
                f"Average memory utilization "
                f"({metrics.memory_average_percent:.2f}%) "
                f"is below the configured upsize "
                f"threshold ({memory_upsize_threshold}%) "
                f"and above the configured downsize "
                f"threshold ({memory_downsize_threshold}%)."
            ),
        )

        self._add_reason(

            analysis,

            "Recommendation",

            "The current VM size remains appropriate based on the configured policy.",
        )

        return analysis