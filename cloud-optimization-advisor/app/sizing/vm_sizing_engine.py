from app.models.azure_vm_sku import (
    AzureVmSku,
)

from app.recommendation.recommendation_action import (
    RecommendationAction,
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

    ####################################################################
    # Public API
    ####################################################################

    def get_candidates(
        self,
        current_vm_size: str,
        recommendation: RecommendationAction,
    ) -> list[AzureVmSku]:

        sku_names = [
            sku.name
            for sku in self.supported_skus
        ]

        if current_vm_size not in sku_names:

            return []

        index = sku_names.index(
            current_vm_size
        )

        #
        # Upsize
        #

        if recommendation == RecommendationAction.UPSIZE:

            return self.supported_skus[
                index + 1 :
            ]

        #
        # Downsize
        #

        if recommendation == RecommendationAction.DOWNSIZE:

            return list(
                reversed(
                    self.supported_skus[
                        :index
                    ]
                )
            )

        #
        # Keep Current Size
        #

        return [
            self.supported_skus[index]
        ]