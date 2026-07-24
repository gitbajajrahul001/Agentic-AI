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
    
    # def _calculate_score(
    #     self,
    #     current: AzureVmSku,
    #     candidate: AzureVmSku,
    # ) -> float:

    #     score = 0.0


    def _cpu_score(
        self,
        current,
        candidate,
    ) -> float:

        difference = abs(

            current.capability_int(
                "vCPUsAvailable"
            )

            -

            candidate.capability_int(
                "vCPUsAvailable"
            )

        )

        return max(
            0,
            40 - difference * 10,
        )
        
        
    def _memory_score(
        self,
        current,
        candidate,
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

        difference = abs(

            current_memory

            -

            candidate_memory

        )

        return max(
            0,
            40 - difference * 2,
        )
        
        
        
        
    def _generation_score(
        self,
        candidate,
    ) -> float:

        name = candidate.name.lower()

        if "v6" in name:
            return 10

        if "v5" in name:
            return 8

        if "v4" in name:
            return 6

        return 4
    
    def _architecture_score(
        self,
        current,
        candidate,
    ) -> float:

        return (

            5

            if

            current.capability(
                "CpuArchitectureType"
            )

            ==

            candidate.capability(
                "CpuArchitectureType"
            )

            else

            0

        )
        
    def _family_score(
        self,
        current,
        candidate,
    ) -> float:

        return (

            5

            if

            current.family

            ==

            candidate.family

            else

            0

        )


    
    def get_candidates(
        self,
        current_sku: AzureVmSku,
        recommendation: RecommendationAction,
    ) -> list[AzureVmSku]:

        ranked_candidates = []

            
        for sku in self.supported_skus:

            if sku.name == current_sku.name:
                continue

            cpu_score = self._cpu_score(
                current_sku,
                sku,
            )

            memory_score = self._memory_score(
                current_sku,
                sku,
            )

            generation_score = self._generation_score(
                sku,
            )

            architecture_score = self._architecture_score(
                current_sku,
                sku,
            )

            family_score = self._family_score(
                current_sku,
                sku,
            )

            total_score = (
                cpu_score
                + memory_score
                + generation_score
                + architecture_score
                + family_score
            )

            ranked_candidates.append(

                RankedVmCandidate(

                    sku=sku,

                    total_score=total_score,

                    cpu_score=cpu_score,

                    memory_score=memory_score,

                    generation_score=generation_score,

                    architecture_score=architecture_score,

                    family_score=family_score,

                )

            )





        ranked_candidates.sort(
            key=lambda candidate: candidate.total_score,
            reverse=True,
        )
        
        print("\nCandidate Ranking")

        for candidate in ranked_candidates:

            print(
                candidate.sku.name,
                candidate.total_score,
            )
            
            print(

                f"{candidate.sku.name:<25}"

                f" Total={candidate.total_score:>5.1f}"

                f" CPU={candidate.cpu_score:>4.0f}"

                f" MEM={candidate.memory_score:>4.0f}"

                f" GEN={candidate.generation_score:>4.0f}"

                f" ARCH={candidate.architecture_score:>3.0f}"

                f" FAM={candidate.family_score:>3.0f}"

            )

        return [

            candidate.sku

            for candidate in ranked_candidates

        ]