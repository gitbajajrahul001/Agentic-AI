from dataclasses import dataclass


@dataclass
class AzureComputeProfile:
    """
    Compute capabilities of the VM.
    """

    vm_size: str = ""

    vcpu_count: int = 0

    memory_gb: float = 0

    max_data_disks: int = 0

    network_bandwidth_mbps: int = 0

    premium_storage_supported: bool = False