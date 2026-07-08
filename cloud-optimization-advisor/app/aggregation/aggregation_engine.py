from app.aggregation.resource_group_aggregator import (
    ResourceGroupAggregator,
)

from app.aggregation.subscription_aggregator import (
    SubscriptionAggregator,
)


class AggregationEngine:

    def run(
        self,
        vm_document_files: list[str],
    ):

        resource_group_aggregator = (
            ResourceGroupAggregator()
        )

        subscription_aggregator = (
            SubscriptionAggregator()
        )

        vm_documents = (
            resource_group_aggregator.load_vm_documents(
                vm_document_files,
            )
        )

        resource_group_documents = (
            resource_group_aggregator.aggregate(
                vm_documents,
            )
        )

        subscription_documents = (
            subscription_aggregator.aggregate(
                [
                    resource_group.model_dump()
                    for resource_group in resource_group_documents
                ]
            )
        )

        return (
            resource_group_documents,
            subscription_documents,
        )