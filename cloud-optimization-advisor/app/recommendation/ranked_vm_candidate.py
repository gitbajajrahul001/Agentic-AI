from dataclasses import dataclass

from app.models.azure_vm_sku import AzureVmSku


@dataclass
class RankedVmCandidate:

    sku: AzureVmSku

    score: float