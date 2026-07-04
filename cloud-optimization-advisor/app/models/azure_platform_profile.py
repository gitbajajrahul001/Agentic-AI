from pydantic import BaseModel


class AzurePlatformProfile(BaseModel):
    """
    Current platform configuration.
    """

    hyperv_generation: str = ""

    cpu_architecture: str = ""

    security_type: str = ""

    ephemeral_os_disk_enabled: bool = False