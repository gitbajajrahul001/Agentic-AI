from pydantic import BaseModel


class VmPrice(BaseModel):
    """
    Azure Retail price for a VM SKU.
    """

    vm_size: str

    region: str

    currency: str

    hourly_price: float