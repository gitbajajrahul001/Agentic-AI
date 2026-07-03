from typing import Optional

from pydantic import BaseModel, Field


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