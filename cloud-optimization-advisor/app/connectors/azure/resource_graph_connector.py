from app.connectors.azure.base_azure_connector import (
    BaseAzureConnector
)

from app.models.azure_virtual_machine import (
    AzureVirtualMachine
)


class ResourceGraphConnector(BaseAzureConnector):
    """
    Azure Resource Graph Connector
    """

    RESOURCE_GRAPH_ENDPOINT = (
        "https://management.azure.com/providers/"
        "Microsoft.ResourceGraph/resources"
        "?api-version=2022-10-01"
    )

    def __init__(
        self,
        credential,
        subscription_ids
    ):

        super().__init__(credential)

        self.subscription_ids = subscription_ids

    def get_virtual_machines(
        self
    ) -> list[AzureVirtualMachine]:

        body = {

            "subscriptions": self.subscription_ids,

            "query": """
Resources
| where type =~ 'microsoft.compute/virtualmachines'
| project
    id,
    name,
    subscriptionId,
    resourceGroup,
    location,
    vmSize=tostring(properties.hardwareProfile.vmSize),
    tags
"""

        }

        response = self._post(
            self.RESOURCE_GRAPH_ENDPOINT,
            body
        )

        virtual_machines = []

        for row in response.get("data", []):

            virtual_machines.append(

                AzureVirtualMachine(

                    id=row["id"],
                    name=row["name"],
                    subscription_id=row["subscriptionId"],
                    resource_group=row["resourceGroup"],
                    location=row["location"],
                    vm_size=row["vmSize"],
                    tags=row.get("tags", {})

                )

            )

        return virtual_machines