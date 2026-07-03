from pydantic import BaseModel


class AzureSecurityProfile(BaseModel):
    """
    Current VM security configuration.
    """

    security_type: str = ""