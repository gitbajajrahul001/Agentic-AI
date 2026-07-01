from rich.console import Console

from app.core.config_loader import ConfigLoader
from app.connectors.azure.authentication_connector import (
    AzureAuthenticationConnector,
)

console = Console()


def main():
    """
    Application Entry Point
    """

    console.rule("[bold blue]Cloud Optimization Advisor[/bold blue]")

    #
    # Load Configuration
    #
    config = ConfigLoader.load()

    console.print(
        "✓ Configuration loaded successfully.",
        style="green"
    )

    #
    # Authenticate to Azure
    #
    authentication_connector = AzureAuthenticationConnector(
        config["azure"]
    )

    credential = authentication_connector.authenticate()

    console.print(
        "✓ Successfully authenticated to Azure.",
        style="green"
    )

    console.print(
        f"Credential Type : {type(credential).__name__}",
        style="cyan"
    )


if __name__ == "__main__":
    main()