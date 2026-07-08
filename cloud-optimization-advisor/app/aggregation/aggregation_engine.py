from app.aggregation.resource_group_aggregator import (
    ResourceGroupAggregator,
)

from app.aggregation.subscription_aggregator import (
    SubscriptionAggregator,
)

from app.aggregation.enterprise_aggregator import (
    EnterpriseAggregator,
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

        enterprise_aggregator = (
            EnterpriseAggregator()
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
        
        enterprise_document = (
            enterprise_aggregator.aggregate(
                [
                    subscription.model_dump()
                    for subscription in subscription_documents
                ]
            )
        )

        return (
            resource_group_documents,
            subscription_documents,
            enterprise_document,
        )
        