from azure.identity import ClientSecretCredential
from azure.core.exceptions import ClientAuthenticationError


class AzureAuthenticationConnector:
    """
    Azure Authentication Connector

    Responsibility
    --------------
    Authenticate to Azure using a Service Principal and return a validated
    Azure credential.

    This connector is responsible ONLY for authentication.

    It does NOT:
        - Query Azure resources
        - Retrieve subscriptions
        - Retrieve virtual machines
        - Execute Resource Graph queries
    """

    def __init__(self, azure_config: dict):
        self.azure_config = azure_config

    def authenticate(self) -> ClientSecretCredential:
        """
        Creates and validates an Azure credential.

        Returns
        -------
        ClientSecretCredential
            A validated Azure credential.

        Raises
        ------
        RuntimeError
            If authentication fails.
        """

        try:

            credential = ClientSecretCredential(
                tenant_id=self.azure_config["tenant_id"],
                client_id=self.azure_config["client_id"],
                client_secret=self.azure_config["client_secret"]
            )

            #
            # Force Azure authentication immediately.
            # Without this call, authentication is "lazy" and
            # failures appear much later.
            #
            credential.get_token(
                "https://management.azure.com/.default"
            )

            return credential

        except ClientAuthenticationError as ex:
            raise RuntimeError(
                f"Azure authentication failed.\n{ex}"
            ) from ex

        except Exception as ex:
            raise RuntimeError(
                f"Unexpected authentication error.\n{ex}"
            ) from ex