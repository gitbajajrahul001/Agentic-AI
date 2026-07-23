from app.models.azure_vm_sku import (
    AzureVmSku,
)

from app.recommendation.recommendation_action import (
    RecommendationAction,
)

from app.recommendation.ranked_vm_candidate import (
    RankedVmCandidate,
)

class VmSizingEngine:
    """
    Generates an ordered list of candidate VM SKUs
    based on the recommendation.

    The sizing engine does NOT validate candidates.

    Validation is performed separately by the
    Validation Engine.
    """

    def __init__(
        self,
        supported_skus: list[AzureVmSku],
    ):

        self.supported_skus = supported_skus


    def _cpu_difference(
        self,
        current: AzureVmSku,
        candidate: AzureVmSku,
    ) -> int:

        return abs(

            current.capability_int("vCPUsAvailable")

            -

            candidate.capability_int("vCPUsAvailable")
        )
        
    def _memory_difference(
        self,
        current: AzureVmSku,
        candidate: AzureVmSku,
    ) -> float:

        current_memory = float(

            current.capability(
                "MemoryGB",
                0,
            )
        )

        candidate_memory = float(

            candidate.capability(
                "MemoryGB",
                0,
            )
        )

        return abs(
            current_memory - candidate_memory
        )
        
    def _architecture_penalty(
        self,
        current: AzureVmSku,
        candidate: AzureVmSku,
    ) -> int:

        current_cpu = current.capability(
            "CpuArchitectureType",
            "",
        )

        candidate_cpu = candidate.capability(
            "CpuArchitectureType",
            "",
        )

        return 0 if current_cpu == candidate_cpu else 10
    
    def _family_penalty(
        self,
        current: AzureVmSku,
        candidate: AzureVmSku,
    ) -> int:

        return 0 if current.family == candidate.family else 10
    
    def _calculate_score(
        self,
        current: AzureVmSku,
        candidate: AzureVmSku,
    ) -> float:

        score = 0.0

        ############################################################
        # CPU Similarity (40)
        ############################################################

        current_cpu = current.capability_int(
            "vCPUsAvailable"
        )

        candidate_cpu = candidate.capability_int(
            "vCPUsAvailable"
        )

        cpu_difference = abs(
            current_cpu - candidate_cpu
        )

        score += max(
            0,
            40 - (cpu_difference * 10),
        )

        ############################################################
        # Memory Similarity (40)
        ############################################################

        current_memory = float(
            current.capability(
                "MemoryGB",
                0,
            )
        )

        candidate_memory = float(
            candidate.capability(
                "MemoryGB",
                0,
            )
        )

        memory_difference = abs(
            current_memory - candidate_memory
        )

        score += max(
            0,
            40 - (memory_difference * 2),
        )

        ############################################################
        # Processor Architecture (5)
        ############################################################

        if (
            current.capability("CpuArchitectureType")
            ==
            candidate.capability("CpuArchitectureType")
        ):
            score += 5

        ############################################################
        # VM Family (5)
        ############################################################

        if current.family == candidate.family:
            score += 5

        ############################################################
        # VM Generation (10)
        ############################################################

        current_name = current.name.lower()

        candidate_name = candidate.name.lower()

        if "v6" in candidate_name:
            score += 10

        elif "v5" in candidate_name:
            score += 8

        elif "v4" in candidate_name:
            score += 6

        elif "v3" in candidate_name:
            score += 4

        return score
    
    def get_candidates(
        self,
        current_sku: AzureVmSku,
        recommendation: RecommendationAction,
    ) -> list[AzureVmSku]:

        ranked_candidates = []

        for sku in self.supported_skus:

            if sku.name == current_sku.name:
                continue

            ranked_candidates.append(

                RankedVmCandidate(

                    sku=sku,

                    score=self._calculate_score(
                        current_sku,
                        sku,
                    ),

                )

            )

        ranked_candidates.sort(
            key=lambda candidate: candidate.score,
            reverse=True,
        )
        
        print("\nCandidate Ranking")

        for candidate in ranked_candidates:

            print(
                f"{candidate.sku.name:<25}"
                f" Score={candidate.score:>5.1f}"
            )

        return [

            candidate.sku

            for candidate in ranked_candidates

        ]