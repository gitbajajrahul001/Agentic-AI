from typing import Optional

from pydantic import BaseModel, Field

from app.models.azure_storage_profile import (
    AzureStorageProfile,
)

from app.models.azure_network_profile import (
    AzureNetworkProfile,
)

from app.models.azure_platform_profile import (
    AzurePlatformProfile,
)


class AzureVirtualMachine(BaseModel):
    """
    Azure Virtual Machine domain model.
    """

    id: str
    name: str
    subscription_id: str
    resource_group: str
    location: str
    vm_size: str
    operating_system: Optional[str] = None
    power_state: Optional[str] = None

    tags: dict[str, str] = Field(default_factory=dict)

    storage_profile: AzureStorageProfile = Field(
        default_factory=AzureStorageProfile
    )

    network_profile: AzureNetworkProfile = Field(
        default_factory=AzureNetworkProfile
    )

    platform_profile: AzurePlatformProfile = Field(
        default_factory=AzurePlatformProfile
)