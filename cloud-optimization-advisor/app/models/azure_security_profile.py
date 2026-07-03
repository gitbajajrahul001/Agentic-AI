from pydantic import BaseModel


class AzureSecurityProfile(BaseModel):
    """
    Current security configuration.
    """

    trusted_launch: bool = False

    confidential_vm: bool = False

    encryption_at_host: bool = False