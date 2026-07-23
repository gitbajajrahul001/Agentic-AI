from azure.mgmt.compute import (
    ComputeManagementClient,
)

from app.connectors.azure.base_azure_connector import (
    BaseAzureConnector,
)

from app.models.azure_vm_sku import (
    AzureVmSku,
)



class VmSkuConnector(BaseAzureConnector):
    """
    Retrieves Azure Virtual Machine SKU information
    from the Azure Resource SKUs API.
    """

    def __init__(
        self,
        credential,
        subscription_id,
    ):

        super().__init__(credential)

        self.client = ComputeManagementClient(
            credential,
            subscription_id,
        )
        
        self.vm_skus: list[AzureVmSku] = []


    ####################################################################
    # VM SKUs
    ####################################################################

    def get_vm_skus(self):
        """
        Returns a unique list of Azure Virtual Machine
        SKUs.

        Azure returns one ResourceSku per location.
        This method removes duplicate entries and
        keeps a single record for each VM SKU.
        """

        skus = list(
            self.client.resource_skus.list()
        )

        unique_skus = {}

        for sku in skus:

            #
            # Ignore non-VM resources.
            #
            if sku.resource_type != "virtualMachines":
                continue

            #
            # Keep only the first occurrence of
            # each VM SKU.
            #
            if sku.name not in unique_skus:

                unique_skus[sku.name] = sku

        #return list(
            #unique_skus.values()
        #)
        vm_skus = []

        for sku in unique_skus.values():

            vm_skus.append(
                self._map_vm_sku(
                    sku
                )
            )

        self.vm_skus = vm_skus

        return self.vm_skus


    ####################################################################
    # Lookup
    ####################################################################

    def get_vm_sku_by_name(
        self,
        sku_name: str,
    ) -> AzureVmSku | None:

        for sku in self.vm_skus:

            if sku.name.lower() == sku_name.lower():
                return sku

        return None




    def _map_vm_sku(
        self,
        sku,
    ) -> AzureVmSku:

        capabilities = {}

        for capability in sku.capabilities:

            capabilities[
             capability.name
            ] = capability.value

        return AzureVmSku(

            name=sku.name,

            family=sku.family,

            size=sku.size,

            tier=sku.tier,

            capabilities=capabilities,
        )