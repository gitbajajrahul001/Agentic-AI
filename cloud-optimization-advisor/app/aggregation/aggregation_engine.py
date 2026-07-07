from app.aggregation.resource_group_aggregator import (
    ResourceGroupAggregator,
)


class AggregationEngine:

    def run(
        self,
        vm_document_files: list[str],
    ):

        aggregator = ResourceGroupAggregator()

        vm_documents = (
            aggregator.load_vm_documents(
                vm_document_files,
            )
        )

        resource_groups = (
            aggregator.aggregate(
                vm_documents,
            )
        )

        for resource_group in resource_groups:

            print()

            print(
                resource_group.model_dump_json(
                    indent=4
                )
            )