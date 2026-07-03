from app.connectors.azure.base_azure_connector import (
    BaseAzureConnector,
)

from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_storage_profile import (
    AzureStorageProfile,
)

from app.models.azure_network_profile import (
    AzureNetworkProfile,
)

from app.models.azure_security_profile import (
    AzureSecurityProfile,
)


class ResourceGraphConnector(BaseAzureConnector):
    """
    Azure Resource Graph Connector.
    """

    RESOURCE_GRAPH_ENDPOINT = (
        "https://management.azure.com/providers/"
        "Microsoft.ResourceGraph/resources"
        "?api-version=2022-10-01"
    )

    def __init__(
        self,
        credential,
        subscription_ids,
    ):

        super().__init__(credential)

        self.subscription_ids = subscription_ids

    ####################################################################
    # Virtual Machines
    ####################################################################

    def get_virtual_machines(
        self,
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
    vmSize = tostring(properties.hardwareProfile.vmSize),
    operatingSystem = tostring(properties.storageProfile.osDisk.osType),
    osDiskType = tostring(properties.storageProfile.osDisk.managedDisk.storageAccountType),
    osDiskSizeGB = toint(properties.storageProfile.osDisk.diskSizeGB),
    dataDiskCount = coalesce(array_length(properties.storageProfile.dataDisks), 0),
    nicCount = coalesce(array_length(properties.networkProfile.networkInterfaces), 0),
    securityType = tostring(properties.securityProfile.securityType),
    powerStateCode = tostring(properties.extended.instanceView.powerState.code),
    powerStateDisplay = tostring(properties.extended.instanceView.powerState.displayStatus),
    identityType = coalesce(tostring(identity.type), 'None'),
    availabilityZone = coalesce(tostring(zones[0]), 'None'),
    tags
"""
        }

        response = self._post(
            self.RESOURCE_GRAPH_ENDPOINT,
            body,
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

                    tags=row.get("tags", {}),

                    storage_profile=AzureStorageProfile(

                        os_disk_type=row.get(
                            "osDiskType",
                            "",
                        ),

                        os_disk_size_gb=row.get(
                            "osDiskSizeGB",
                            0,
                        ),

                        data_disk_count=row.get(
                            "dataDiskCount",
                            0,
                        ),

                        has_premium_ssd=(
                            row.get("osDiskType")
                            == "Premium_LRS"
                        ),

                        has_ultra_ssd=(
                            row.get("osDiskType")
                            == "UltraSSD_LRS"
                        ),
                    ),

                    network_profile=AzureNetworkProfile(

                        nic_count=row.get(
                            "nicCount",
                            0,
                        ),

                        #
                        # Resource Graph does not expose
                        # Accelerated Networking.
                        #
                        accelerated_networking=False,
                    ),

                    security_profile=AzureSecurityProfile(

                        security_type=row.get(
                            "securityType",
                            "",
                        ),
                    ),
                )
            )

        return virtual_machines