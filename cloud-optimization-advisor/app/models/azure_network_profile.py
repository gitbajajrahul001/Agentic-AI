from pydantic import BaseModel


class AzureNetworkProfile(BaseModel):
    """
    Current network configuration.
    """

    accelerated_networking_enabled: bool = False

    network_interface_count: int = 0