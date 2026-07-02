from app.connectors.azure.base_azure_connector import (
    BaseAzureConnector
)


class MetricsDefinitionConnector(
    BaseAzureConnector
):
    """
    Discover available Azure Monitor metrics.
    """

    API_VERSION = "2023-10-01"

    def __init__(
        self,
        credential
    ):

        super().__init__(credential)

    def get_metric_definitions(
        self,
        resource_id: str
    ) -> dict:

        endpoint = (
            f"https://management.azure.com{resource_id}"
            f"/providers/microsoft.insights/"
            f"metricDefinitions"
            f"?api-version={self.API_VERSION}"
        )

        return self._get(endpoint)