from collections import defaultdict
from pathlib import Path
import json


class ResourceGroupAggregator:

    def load_vm_documents(
        self,
        vm_document_files: list[str],
    ) -> list[dict]:

        vm_documents = []

        for file in vm_document_files:

            with open(
                file,
                "r",
                encoding="utf-8",
            ) as f:

                vm_documents.append(
                    json.load(f)
                )

        return vm_documents 
       
    
    def aggregate(
        self,
        vm_documents: list[dict],
    ):

        grouped_documents = defaultdict(list)

        for vm in vm_documents:

            resource_group = (
                vm["inventory"]["resource_group"]
            )

            grouped_documents[
                resource_group
            ].append(
                vm
            )

        return grouped_documents