from app.models.azure_vm_sku import (
    AzureVmSku,
)

from app.recommendation.recommendation_action import (
    RecommendationAction,
)


class VmSizingEngine:
    """
    Determines the recommended VM SKU based on
    the recommendation action.

    Version 1:
    - Uses only the organization supported SKU order.
    - No capability validation.
    """

    def __init__(
        self,
        supported_skus: list[AzureVmSku],
    ):

        self.supported_skus = supported_skus

    ####################################################################
    # Public API
    ####################################################################

    def recommend_size(
        self,
        current_vm_size: str,
        recommendation: RecommendationAction,
    ) -> AzureVmSku | None:

        #
        # Find current SKU index.
        #

        sku_names = [
            sku.name
            for sku in self.supported_skus
        ]

        if current_vm_size not in sku_names:

            return None

        index = sku_names.index(
            current_vm_size
        )

        #
        # Upsize
        #

        if recommendation == RecommendationAction.UPSIZE:

            if index < len(sku_names) - 1:

                return self.supported_skus[
                    index + 1
                ]

            return self.supported_skus[index]

        #
        # Downsize
        #

        if recommendation == RecommendationAction.DOWNSIZE:

            if index > 0:

                return self.supported_skus[
                    index - 1
                ]

            return self.supported_skus

        #
        # Keep
        #

        return self.supported_skus[
            index
        ]