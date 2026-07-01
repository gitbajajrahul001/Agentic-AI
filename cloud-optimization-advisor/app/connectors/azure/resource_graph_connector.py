import requests

from app.models.azure_virtual_machine import AzureVirtualMachine


class ResourceGraphConnector:
    """
    Azure Resource Graph Connector

    Responsibility
    --------------
    Retrieve Azure Virtual Machine inventory
    using Azure Resource Graph REST API.
    """

    RESOURCE_GRAPH_ENDPOINT = (
        "https://management.azure.com/providers/"
        "Microsoft.ResourceGraph/resources"
        "?api-version=2022-10-01"
    )

    def __init__(self, credential, subscription_ids):

        self.credential = credential
        self.subscription_ids = subscription_ids

    def get_virtual_machines(self) -> list[AzureVirtualMachine]:

        token = self.credential.get_token(
            "https://management.azure.com/.default"
        )

        headers = {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        }

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

        response = requests.post(
            self.RESOURCE_GRAPH_ENDPOINT,
            headers=headers,
            json=body,
            timeout=60
        )

        response.raise_for_status()

        data = response.json()

        virtual_machines = []

        for row in data.get("data", []):

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