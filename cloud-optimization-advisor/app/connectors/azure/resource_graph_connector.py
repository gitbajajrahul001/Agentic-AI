from azure.mgmt.resourcegraph import ResourceGraphClient
from azure.mgmt.resourcegraph.models import QueryRequest

from app.models.azure_virtual_machine import AzureVirtualMachine


class ResourceGraphConnector:
    """
    Azure Resource Graph Connector

    Responsibility
    --------------
    Retrieve Azure Virtual Machine inventory using Azure Resource Graph.

    Returns
    -------
    list[AzureVirtualMachine]
    """

    def __init__(self, credential, subscription_ids):

        self.client = ResourceGraphClient(credential)
        self.subscription_ids = subscription_ids

    def get_virtual_machines(self):

        query = """
        Resources
        | where type =~ 'microsoft.compute/virtualmachines'
        | project
            id,
            name,
            subscriptionId,
            resourceGroup,
            location,
            vmSize = tostring(properties.hardwareProfile.vmSize),
            tags
        """

        request = QueryRequest(
            subscriptions=self.subscription_ids,
            query=query
        )

        response = self.client.resources(request)

        virtual_machines = []

        for row in response.data:

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