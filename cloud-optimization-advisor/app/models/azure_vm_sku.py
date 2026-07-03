from pydantic import BaseModel, Field


class AzureVmSku(BaseModel):
    """
    Azure Virtual Machine SKU.
    """

    name: str

    family: str

    size: str

    tier: str

    capabilities: dict[str, str] = Field(
        default_factory=dict
    )

    ####################################################################
    # Helpers
    ####################################################################

    def capability(
        self,
        name: str,
        default=None,
    ):
        return self.capabilities.get(
            name,
            default,
        )

    def capability_int(
        self,
        name: str,
        default: int = 0,
    ) -> int:

        value = self.capabilities.get(name)

        return int(value) if value else default

    def capability_bool(
        self,
        name: str,
        default: bool = False,
    ) -> bool:

        value = self.capabilities.get(name)

        if value is None:
            return default

        return value.lower() == "true"