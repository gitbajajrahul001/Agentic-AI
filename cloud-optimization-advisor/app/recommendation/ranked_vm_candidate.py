from dataclasses import dataclass

from app.models.azure_vm_sku import (
    AzureVmSku,
)


@dataclass
class RankedVmCandidate:

    sku: AzureVmSku

    total_score: float

    cpu_score: float

    memory_score: float

    generation_score: float

    architecture_score: float

    family_score: float