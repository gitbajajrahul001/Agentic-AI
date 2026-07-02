from pydantic import BaseModel


class AzureVirtualMachineMetrics(BaseModel):
    """
    Runtime telemetry collected for an Azure Virtual Machine.

    This model contains observed behaviour of the VM.
    It does NOT contain inventory information such as
    name, location or VM size.
    """

    #
    # CPU
    #

    cpu_average_percent: float = 0.0
    cpu_max_percent: float = 0.0
    cpu_p95_percent: float = 0.0

    #
    # Memory
    #

    memory_average_percent: float = 0.0
    memory_max_percent: float = 0.0
    memory_p95_percent: float = 0.0

    #
    # Network
    #

    network_in_average_bytes: float = 0.0
    network_out_average_bytes: float = 0.0

    #
    # Disk
    #

    disk_read_average_bytes: float = 0.0
    disk_write_average_bytes: float = 0.0

    #
    # Telemetry Quality
    #

    sample_count: int = 0

    telemetry_coverage_percent: float = 0.0