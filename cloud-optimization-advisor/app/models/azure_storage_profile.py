from pydantic import BaseModel


class AzureStorageProfile(BaseModel):
    """
    Current storage configuration attached to the VM.
    """

    os_disk_type: str = ""

    os_disk_size_gb: int = 0

    data_disk_count: int = 0

    has_premium_ssd: bool = False

    has_ultra_ssd: bool = False