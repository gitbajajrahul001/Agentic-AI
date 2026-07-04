from pydantic import Field

from pydantic import BaseModel, Field

from app.models.azure_virtual_machine import (
    AzureVirtualMachine,
)

from app.models.azure_virtual_machine_metrics import (
    AzureVirtualMachineMetrics,
)

from app.models.VirtualMachineAnalysis import (
    VirtualMachineAnalysis,
)

from app.models.cost_analysis import (
    CostAnalysis,
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
    
    cost_analysis: CostAnalysis = Field(
    default_factory=CostAnalysis    
    
    )
       
    metadata: dict[str, str] = Field(
        default_factory=dict
    )


