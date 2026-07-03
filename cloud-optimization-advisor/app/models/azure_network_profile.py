from pydantic import BaseModel


class AzureNetworkProfile(BaseModel):
    """
    Current network configuration.
    """

    nic_count: int = 0

    accelerated_networking: bool = False