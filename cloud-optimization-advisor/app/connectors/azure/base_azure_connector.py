import requests


class BaseAzureConnector:
    """
    Base class for all Azure REST API connectors.

    Responsibilities
    ----------------
    - Acquire Azure access tokens
    - Build authorization headers
    - Execute HTTP GET requests
    - Execute HTTP POST requests

    Child connectors should focus only on
    business logic.
    """

    MANAGEMENT_SCOPE = "https://management.azure.com/.default"

    DEFAULT_TIMEOUT = 60

    def __init__(self, credential):

        self.credential = credential

    def _get_headers(self) -> dict:
        """
        Build Azure authorization headers.
        """

        token = self.credential.get_token(
            self.MANAGEMENT_SCOPE
        )

        return {
            "Authorization": f"Bearer {token.token}",
            "Content-Type": "application/json"
        }

    def _get(
        self,
        url: str,
        params: dict | None = None
    ) -> dict:
        """
        Execute HTTP GET request.
        """

        response = requests.get(
            url,
            headers=self._get_headers(),
            params=params,
            timeout=self.DEFAULT_TIMEOUT
        )

        response.raise_for_status()

        return response.json()

    def _post(
        self,
        url: str,
        body: dict
    ) -> dict:
        """
        Execute HTTP POST request.
        """

        response = requests.post(
            url,
            headers=self._get_headers(),
            json=body,
            timeout=self.DEFAULT_TIMEOUT
        )

        response.raise_for_status()

        return response.json()