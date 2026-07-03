from pydantic import BaseModel

from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_virtual_machine_metrics import (
    AzureVirtualMachineMetrics,
)

from app.models.VirtualMachineAnalysis import (
    VirtualMachineAnalysis,
)


class VMOptimizationReport(BaseModel):
    """
    Represents the complete optimization report
    for a single virtual machine.

    Combines inventory, telemetry and analysis
    into a single object for rendering.
    """

    virtual_machine: AzureVirtualMachine

    metrics: AzureVirtualMachineMetrics

    analysis: VirtualMachineAnalysis